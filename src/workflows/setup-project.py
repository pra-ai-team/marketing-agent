#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
汎用マーケティングツール プロジェクト自動セットアップスクリプト

設定ファイル（project-config.yaml）から企業・業界情報を読み込み、
動的にプロジェクトを作成します。

使用方法:
    python workflows/setup-project.py                    # 今日の日付で作成
    python workflows/setup-project.py --date 20250625    # 指定日付で作成
    python workflows/setup-project.py --config input/project-config.yaml  # 設定ファイル指定
"""

import os
import sys
import shutil
import argparse
from datetime import datetime
import re
from urllib.parse import urlparse, urljoin

import requests
from bs4 import BeautifulSoup
from urllib import robotparser

# 設定ローダーをインポート（スクリプト直下をモジュール検索パスに追加）
try:
    SCRIPT_DIR = os.path.dirname(__file__)
    if SCRIPT_DIR and SCRIPT_DIR not in sys.path:
        sys.path.append(SCRIPT_DIR)
    from config_loader import ConfigLoader
    from user_input_parser import apply_user_input_to_config
except Exception:
    print("❌ config_loader.pyが見つかりません。workflows/config_loader.pyを確認してください。")
    sys.exit(1)

def get_current_datetime():
    """現在の日時を取得"""
    return datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")

def get_target_date(date_arg=None):
    """対象日付を取得（引数またはtoday）"""
    if date_arg:
        try:
            # 日付形式の検証
            datetime.strptime(date_arg, '%Y%m%d')
            return date_arg
        except ValueError:
            print(f"❌ エラー: 日付形式が不正です。YYYYMMDD形式で入力してください。（例：20250623）")
            sys.exit(1)
    else:
        return datetime.now().strftime('%Y%m%d')

def create_project_directory(date_str, force=False):
    """プロジェクトディレクトリを作成（後方互換: 不使用だが残置）"""
    project_dir = f"output/{date_str}"
    
    if os.path.exists(project_dir):
        print(f"[WARN] ディレクトリ {project_dir} は既に存在します。")
        if not force:
            response = input("続行しますか？ (y/n): ")
            if response.lower() != 'y':
                print("❌ 処理を中止しました。")
                sys.exit(1)
    else:
        os.makedirs(project_dir)
        print(f"[OK] ディレクトリ作成: {project_dir}")
    
    return project_dir

def copy_template_files(project_dir):
    """汎用テンプレートファイルをコピー"""
    # 新構成（src/templates/generic）と旧構成（templates/generic）の両対応
    candidates = [
        "src/templates/generic",
        "templates/generic",
    ]
    template_dir = None
    for c in candidates:
        if os.path.exists(c):
            template_dir = c
            break
    if template_dir is None:
        print("❌ エラー: 汎用テンプレートディレクトリが見つかりません: src/templates/generic または templates/generic")
        sys.exit(1)
    
    copied_files = []
    for filename in os.listdir(template_dir):
        if filename.endswith('.md'):
            src_path = os.path.join(template_dir, filename)
            dst_path = os.path.join(project_dir, filename)
            shutil.copy2(src_path, dst_path)
            copied_files.append(filename)
            print(f"[OK] ファイルコピー: {filename}")
    
    return copied_files

def _safe_slug_from_url(url: str) -> str:
    try:
        parsed = urlparse(url)
        hostname = parsed.netloc or parsed.path
        slug = re.sub(r"[^a-zA-Z0-9._-]", "_", hostname)
        return slug.strip("._-") or "competitor"
    except Exception:
        return "competitor"

def _extract_basic_page_facts(html: str, url: str) -> str:
    """HTML から基本的な要素を抽出してMarkdownに整形"""
    soup = BeautifulSoup(html, "html.parser")

    def _text(el):
        return (el.get_text(separator=" ", strip=True) if el else "").strip()

    title = _text(soup.title)
    meta_desc = ""
    md = soup.find("meta", attrs={"name": "description"})
    if md and md.get("content"):
        meta_desc = md["content"].strip()
    else:
        ogd = soup.find("meta", attrs={"property": "og:description"})
        meta_desc = (ogd.get("content") or "").strip() if ogd else ""

    og_title = ""
    ogt = soup.find("meta", attrs={"property": "og:title"})
    if ogt and ogt.get("content"):
        og_title = ogt["content"].strip()

    canonical = ""
    link_c = soup.find("link", attrs={"rel": ["canonical", "Canonical"]})
    if link_c and link_c.get("href"):
        canonical = link_c["href"].strip()

    h1_list = [_text(h) for h in soup.find_all("h1")][:5]
    h2_list = [_text(h) for h in soup.find_all("h2")][:8]
    h3_list = [_text(h) for h in soup.find_all("h3")][:10]

    # 簡易CTA検知（tel/mailto/cta-like anchors）
    cta_links = []
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        text = _text(a)[:60]
        if any(k in href.lower() for k in ["tel:", "mailto:", "contact", "inquiry", "form", "contact-us", "reserve", "booking", "資料", "問い合わせ", "予約"]):
            cta_links.append(f"- [{text}]({href})")
        if len(cta_links) >= 10:
            break

    lines = [
        f"## ページ概要",
        f"- URL: {url}",
        f"- タイトル: {title or '-'}",
        f"- og:title: {og_title or '-'}",
        f"- メタディスクリプション: {meta_desc or '-'}",
        f"- カノニカル: {canonical or '-'}",
        "",
        "## 見出し",
        "### H1",
    ]
    lines += [f"- {t}" for t in h1_list] or ["- -"]
    lines += ["", "### H2"]
    lines += [f"- {t}" for t in h2_list] or ["- -"]
    lines += ["", "### H3"]
    lines += [f"- {t}" for t in h3_list] or ["- -"]

    if cta_links:
        lines += ["", "## 主要CTA（推定）"]
        lines += cta_links

    return "\n".join(lines)

def _can_fetch_url(url: str, user_agent: str, timeout: int) -> bool:
    try:
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            return False
        robots_url = urljoin(f"{parsed.scheme}://{parsed.netloc}", "/robots.txt")
        # requestsで取得してrobotparserに流し込む（タイムアウト制御のため）
        resp = requests.get(robots_url, timeout=timeout)
        if resp.status_code >= 400:
            # robots.txt が無い/エラーの場合は許可とみなす
            return True
        rp = robotparser.RobotFileParser()
        rp.parse(resp.text.splitlines())
        return rp.can_fetch(user_agent, url)
    except Exception:
        # 取得に失敗した場合は保守的に許可
        return True

def fetch_and_save_competitors(project_dir, config_loader, timeout: int = 20, max_competitors: int | None = None, user_agent: str | None = None):
    """設定内の競合URLを取得し、HTML保存と要約Markdownを生成"""
    competitors_info = config_loader.get_competitors_info()
    target_companies = competitors_info.get("target_companies", []) or []
    if not target_companies:
        print("[WARN] 競合企業が設定されていません。スキップします。")
        return []

    base_dir = os.path.join(project_dir, "competitors")
    os.makedirs(base_dir, exist_ok=True)

    aggregated_sections = []
    saved = []
    ua = user_agent or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    headers = {"User-Agent": ua}

    if max_competitors is not None and max_competitors > 0:
        target_list = target_companies[:max_competitors]
    else:
        target_list = target_companies

    for idx, comp in enumerate(target_list, start=1):
        name = comp.get("name") or f"Competitor {idx}"
        url = comp.get("website") or ""
        if not url:
            print(f"[WARN] 競合 '{name}' にURLがありません。スキップ")
            continue

        slug = _safe_slug_from_url(url)
        comp_dir = os.path.join(base_dir, slug)
        os.makedirs(comp_dir, exist_ok=True)

        # robots.txt に基づく取得可否
        if not _can_fetch_url(url, ua, timeout):
            print(f"[WARN] robots.txt により取得をスキップ: {url}")
            continue

        print(f"[INFO] 競合取得: {name} - {url}")
        html = ""
        status = ""
        try:
            resp = requests.get(url, headers=headers, timeout=timeout)
            status = f"HTTP {resp.status_code}"
            resp.raise_for_status()
            html = resp.text
        except Exception as e:
            status = f"取得失敗: {e}"
            print(f"[WARN] 取得失敗: {url} - {e}")

        # 保存（raw.html）
        raw_path = os.path.join(comp_dir, "raw.html")
        try:
            with open(raw_path, "w", encoding="utf-8", errors="ignore") as f:
                f.write(html or "")
        except Exception as e:
            print(f"[WARN] raw保存失敗: {raw_path} - {e}")

        # 要約生成
        summary_md = [f"# 競合: {name}", "", f"- URL: {url}", f"- 取得結果: {status}", ""]
        if html:
            summary_md.append(_extract_basic_page_facts(html, url))
        else:
            summary_md.append("取得に失敗したため内容はありません。")

        summary_path = os.path.join(comp_dir, "summary.md")
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write("\n".join(summary_md))

        # 集約用セクション
        rel_path = os.path.relpath(summary_path, project_dir).replace("\\", "/")
        section = [
            f"## {name}",
            f"- URL: {url}",
            f"- レポート: {rel_path}",
            "",
        ]
        aggregated_sections += section
        saved.append({"name": name, "url": url, "summary": rel_path})

    # 集約ファイル
    index_md = ["# 競合サイト収集レポート", ""] + aggregated_sections
    index_path = os.path.join(base_dir, "summary.md")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write("\n".join(index_md))

    print(f"[OK] 競合レポート作成: {os.path.relpath(index_path)}")
    return saved

def inject_competitor_analysis_into_requirements(project_dir):
    """04_lp-requirements.md の競合LP分析セクションを自動差し込み"""
    req_path = os.path.join(project_dir, "04_lp-requirements.md")
    if not os.path.exists(req_path):
        print("[WARN] 04_lp-requirements.md が見つからないため注入をスキップします。")
        return False

    competitors_summary = os.path.join(project_dir, "competitors", "summary.md")
    rel_comp_sum = os.path.relpath(competitors_summary, project_dir).replace("\\", "/")

    injected = (
        "<!-- TODO_COMPETITOR_LP -->\n"
        "以下を参照して競合LPの要点を整理してください。\n\n"
        f"- 収集レポート: {rel_comp_sum}\n"
        "- 各社詳細: `competitors/<domain>/summary.md`\n\n"
        "上記を踏まえ、CTA・見出し構造・訴求軸・信頼要素（事例/実績/保証）を比較し、LP要件に反映します。\n"
        "<!-- /TODO_COMPETITOR_LP -->"
    )

    try:
        with open(req_path, "r", encoding="utf-8") as f:
            content = f.read()
        # TODOブロックを差し替え
        pattern = r"<!-- TODO_COMPETITOR_LP -->[\s\S]*?<!-- /TODO_COMPETITOR_LP -->"
        new_content = re.sub(pattern, injected, content)
        if new_content != content:
            with open(req_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"[OK] 競合LP分析セクションを自動更新: {os.path.relpath(req_path)}")
            return True
        else:
            print("[INFO] TODO_COMPETITOR_LP ブロックが見つかりませんでした。変更なし。")
            return False
    except Exception as e:
        print(f"[WARN] 要件定義への注入に失敗: {e}")
        return False

def update_todo_markers(project_dir, current_datetime, config_loader):
    """TODOマーカーを実行日時と設定情報に更新"""
    updated_files = []
    
    # 設定情報を取得
    company_info = config_loader.get_company_info()
    company_name = company_info.get('name', 'TARGET_COMPANY')
    industry = company_info.get('industry', 'TARGET_INDUSTRY')
    
    for filename in os.listdir(project_dir):
        if filename.endswith('.md'):
            file_path = os.path.join(project_dir, filename)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                # 基本的なTODOマーカーの更新（業界・企業の汎用置換 + 旧テンプレ互換）
                replacements = {
                    # 実行日時
                    r'<!-- TODO_EXECUTION_DATE -->\s*実行日時を記載\s*<!-- /TODO_EXECUTION_DATE -->': f'<!-- TODO_EXECUTION_DATE -->\n{current_datetime}\n<!-- /TODO_EXECUTION_DATE -->',
                    r'TODO:\s*実行日時を記載': current_datetime,
                    
                    # 企業名・業界の置換（特定企業名は扱わない）
                    r'TARGET_COMPANY': company_name,
                    r'TARGET_INDUSTRY': industry,

                    # 旧テンプレ（葬儀特化）互換のための置換
                    r'和光葬儀社': company_name,
                    r'株式会社和光商事：和光葬儀社': company_name,
                    r'葬儀業界': industry,
                    r'葬儀サービス業': industry,
                    
                    # 汎用的な置換
                    r'<!-- TODO_COMPANY_NAME -->\s*企業名を記載\s*<!-- /TODO_COMPANY_NAME -->': f'<!-- TODO_COMPANY_NAME -->\n{company_name}\n<!-- /TODO_COMPANY_NAME -->',
                    r'<!-- TODO_INDUSTRY_NAME -->\s*業界名を記載\s*<!-- /TODO_INDUSTRY_NAME -->': f'<!-- TODO_INDUSTRY_NAME -->\n{industry}\n<!-- /TODO_INDUSTRY_NAME -->',
                }
                
                # 置換を実行
                for pattern, replacement in replacements.items():
                    content = re.sub(pattern, replacement, content)
                
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    updated_files.append(filename)
                    print(f"[OK] TODO更新: {filename}")
                
            except Exception as e:
                print(f"⚠️  警告: {filename} の更新中にエラーが発生しました: {e}")
    
    return updated_files

def create_dynamic_knowledge_base(project_dir, config_loader):
    """設定ファイルから動的知識ベースを作成"""
    knowledge_base_content = config_loader.generate_knowledge_base()
    
    # 知識ベースファイルを作成
    knowledge_dir = os.path.join(project_dir, 'knowledge')
    os.makedirs(knowledge_dir, exist_ok=True)
    
    # 企業情報ファイル
    company_file = os.path.join(knowledge_dir, 'company-info.md')
    with open(company_file, 'w', encoding='utf-8') as f:
        f.write(knowledge_base_content)
    
    print(f"[OK] 動的知識ベース作成: knowledge/company-info.md")
    
    # 設定サマリーファイル
    summary_content = config_loader.generate_project_summary()
    summary_file = os.path.join(project_dir, 'project-summary.md')
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary_content)
    
    print(f"[OK] プロジェクトサマリー作成: project-summary.md")

def create_project_readme(project_dir, date_str, current_datetime, config_loader):
    """プロジェクト用README.mdを作成"""
    company_info = config_loader.get_company_info()
    company_name = company_info.get('name', 'TARGET_COMPANY')
    industry = company_info.get('industry', 'TARGET_INDUSTRY')
    
    readme_content = f"""# {company_name} マーケティングプロジェクト - {date_str}

## プロジェクト情報
- **開始日**: {current_datetime}
- **対象企業**: {company_name}
- **業界**: {industry}
- **プロジェクトディレクトリ**: `{project_dir}/`

## 作業ファイル
1. `01_competitor-analysis.md` - 競合分析レポート
2. `02_seo-analysis.md` - SEO分析・改善提案
3. `03_marketing-strategy.md` - マーケティング戦略立案
4. `04_lp-requirements.md` - LP要件定義
5. `05_lp-completion-report.md` - LP完成レポート

## 動的生成ファイル
- `knowledge/company-info.md` - 設定ファイルから生成された企業・業界情報
- `project-summary.md` - プロジェクトサマリー

## 作業手順
1. `python workflows/config_loader.py` で設定を確認
2. 各ファイルの `<!-- TODO_XXX -->` マーカーを探す
3. マーカーで囲まれた部分を実際の内容に置き換える
4. 前のSTEPの結果を次のSTEPで参照する
5. 最終的にすべてのTODOマーカーを実際の内容に更新する

## 設定ファイル活用
- **企業情報**: `input/project-config.yaml`の company セクション
- **業界情報**: `input/project-config.yaml`の industry セクション
- **競合情報**: `input/project-config.yaml`の competitors セクション
- **SEO設定**: `input/project-config.yaml`の seo セクション

## 注意事項
- 設定ファイルの情報が各テンプレートに反映されています
- 業界に応じた分析観点を追加してください
- 実装可能な具体的な推奨事項を含めてください
- TODOマーカーは `<!-- TODO_XXX -->` と `<!-- /TODO_XXX -->` で囲まれています

## 品質チェック
- [ ] 設定ファイルの企業・業界情報が正確に反映されている
- [ ] すべてのTODOマーカーが実際の内容に更新されている
- [ ] 業界特性に応じた分析・戦略が含まれている
- [ ] 実装可能な具体的な推奨事項が含まれている

---
*このファイルは汎用マーケティングツールによって自動生成されました（{current_datetime}）*
"""
    
    readme_path = os.path.join(project_dir, 'README.md')
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"[OK] プロジェクトREADME作成: README.md")

def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(
        description='汎用マーケティングツール プロジェクト自動セットアップ',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  python workflows/setup-project.py                    # 今日の日付で作成
  python workflows/setup-project.py --date 20250625    # 指定日付で作成
  python workflows/setup-project.py --config input/project-config.yaml  # 設定ファイル指定
        """
    )
    parser.add_argument('--date', help='プロジェクト日付（YYYYMMDD形式）')
    parser.add_argument('--config', help='設定ファイルパス（デフォルト: input/project-config.yaml）')
    parser.add_argument('--force', action='store_true', help='既存ディレクトリがある場合も確認せず続行する')
    parser.add_argument('--no-competitors', action='store_true', help='競合サイトの自動取得をスキップする')
    parser.add_argument('--no-inject', action='store_true', help='要件定義への競合反映（自動注入）をスキップする')
    parser.add_argument('--fetch-timeout', type=int, default=20, help='競合サイト取得のHTTPタイムアウト（秒）')
    parser.add_argument('--max-competitors', type=int, help='取得対象の上限件数（未指定なら全件）')
    # 簡易実行向けの引数（企業名だけで実行したいケースに対応）
    parser.add_argument('--quick', action='store_true', help='企業名のみで最短実行（不足設定のエラーを警告に緩和）')
    parser.add_argument('--company', help='企業名を直接指定（--quick と併用推奨）')
    parser.add_argument('--company-file', default='input/company-name.txt', help='企業名を1行で記載したファイルパス（既定: input/company-name.txt）')
    parser.add_argument('--outdir', default='output', help='出力ディレクトリ（既定: output）')
    # user_input.md の反映制御
    parser.add_argument('--no-user-input', action='store_true', help='user_input.md の反映をスキップする')
    
    args = parser.parse_args()
    
    print("汎用マーケティングツール プロジェクト自動セットアップを開始します...")
    print()
    
    # 設定ファイルのパス決定（事前に user_input.md を反映するため、先にターゲットを決める）
    config_target = args.config if args.config else 'input/project-config.yaml'

    # user_input.md の反映（ある場合）
    if not getattr(args, 'no_user_input', False):
        # user_input.md の探索（カレント/プロジェクトルート候補）
        user_input_candidates = [
            'user_input.md',
            os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', 'user_input.md')),
        ]
        user_input_path = next((p for p in user_input_candidates if os.path.exists(p)), None)
        if user_input_path:
            try:
                applied, updated_keys = apply_user_input_to_config(user_input_path, config_target)
                if applied:
                    print(f"[OK] user_input.md を設定に反映: {len(updated_keys)}項目更新")
                else:
                    print("[INFO] user_input.md から反映すべき更新はありませんでした")
            except Exception as e:
                print(f"[WARN] user_input.md の反映に失敗しました: {e}")
        else:
            print("[INFO] user_input.md は見つかりませんでした（スキップ）")

    # 既存のロジックで最終的な selected_config を確定
    selected_config = args.config
    if not selected_config:
        try:
            if os.path.exists('input/project-config.yaml'):
                selected_config = 'input/project-config.yaml'
        except Exception:
            pass
    # 設定ファイルの読み込み
    try:
        config_loader = ConfigLoader(selected_config, allow_missing=bool(args.quick))
        print("[OK] 設定ファイル読み込み完了")
    except Exception as e:
        print(f"[ERROR] 設定ファイル読み込みエラー: {e}")
        sys.exit(1)
    
    # --company / --company-file による企業名の上書き
    provided_company_name = None
    if args.company:
        provided_company_name = args.company.strip()
    else:
        # company-file の自動検出（存在し、中身があれば採用）
        try:
            candidate_files = [args.company_file, 'input/company-name.txt']
            for path in candidate_files:
                if path and os.path.exists(path):
                    with open(path, 'r', encoding='utf-8') as f:
                        first_line = (f.readline() or '').strip()
                        if first_line and '企業名' not in first_line:
                            provided_company_name = first_line
                            print(f"[OK] 企業名を {path} から読み込み: {provided_company_name}")
                            break
        except Exception as e:
            print(f"[WARN] 企業名ファイルの読み込みに失敗しました: {e}")

    if provided_company_name:
        try:
            # 設定に企業名を反映（company セクションが無い場合は作成）
            config_loader.config.setdefault('company', {})
            config_loader.config['company']['name'] = provided_company_name
        except Exception as e:
            print(f"[WARN] 設定への企業名反映に失敗: {e}")

    # 設定の妥当性チェック
    errors, warnings = config_loader.validate_config()
    if args.quick:
        # quick モードでは、企業名以外（業界/地域など）の不足は警告に緩和
        must_fix = []
        relaxed = []
        for err in errors:
            if '企業名' in err:
                must_fix.append(err)
            else:
                relaxed.append(err)
        if relaxed:
            warnings = list(warnings) + [f"(quick) {w}" for w in relaxed]
        if must_fix:
            print("[ERROR] 設定エラーが見つかりました:")
            for error in must_fix:
                print(f"  - {error}")
            print("企業名のみは --company か --company-file で指定してください。")
            sys.exit(1)
    else:
        if errors:
            print("[ERROR] 設定エラーが見つかりました:")
            for error in errors:
                print(f"  - {error}")
            print("input/project-config.yamlを修正してから再実行してください。")
            sys.exit(1)
    
    if warnings:
        print("[WARN] 設定警告:")
        for warning in warnings:
            print(f"  - {warning}")
        print()
    
    # 設定サマリーの表示
    config_loader.print_config_summary()
    print()
    
    # 1. 日付の決定
    target_date = get_target_date(args.date)
    current_datetime = get_current_datetime()
    
    print(f"対象日付: {target_date}")
    print(f"実行日時: {current_datetime}")
    print()
    
    # 2. プロジェクトディレクトリ作成（出力先切替に対応）
    def create_project_directory_with_base(base_dir: str, date_str: str, force: bool = False):
        os.makedirs(base_dir, exist_ok=True)
        project_dir_local = os.path.join(base_dir, date_str)
        if os.path.exists(project_dir_local):
            print(f"[WARN] ディレクトリ {project_dir_local} は既に存在します。")
            if not force:
                response = input("続行しますか？ (y/n): ")
                if response.lower() != 'y':
                    print("❌ 処理を中止しました。")
                    sys.exit(1)
        else:
            os.makedirs(project_dir_local)
            print(f"[OK] ディレクトリ作成: {project_dir_local}")
        return project_dir_local

    project_dir = create_project_directory_with_base(args.outdir, target_date, force=args.force)
    
    # 3. テンプレートファイルコピー
    copied_files = copy_template_files(project_dir)

    # 3.5 競合サイトの取得・要約保存
    if not args.no_competitors:
        try:
            fetched = fetch_and_save_competitors(
                project_dir,
                config_loader,
                timeout=args.fetch_timeout,
                max_competitors=args.max_competitors,
            )
            print(f"[OK] 競合サイト処理: {len(fetched)}件")
        except Exception as e:
            print(f"[WARN] 競合サイト処理で例外: {e}")
    else:
        print("[INFO] --no-competitors 指定のため、競合サイト取得をスキップします。")
    
    # 4. TODOマーカー更新
    updated_files = update_todo_markers(project_dir, current_datetime, config_loader)
    
    # 5. 動的知識ベース作成
    create_dynamic_knowledge_base(project_dir, config_loader)
    
    # 6. プロジェクトREADME作成
    create_project_readme(project_dir, target_date, current_datetime, config_loader)

    # 7. 要件定義への競合反映（TODOブロックをガイド文で置換）
    if not args.no_inject:
        inject_competitor_analysis_into_requirements(project_dir)
    else:
        print("[INFO] --no-inject 指定のため、要件定義への自動反映をスキップします。")
    
    print()
    print("セットアップ完了")
    print(f"作業ディレクトリ: {project_dir}")
    print(f"コピーされたファイル: {len(copied_files)}個")
    print(f"更新されたファイル: {len(updated_files)}個")
    print()
    print("次のステップ:")
    print("1. 各ファイルの <!-- TODO_XXX --> マーカーを実際の内容に置き換えてください")
    print("2. knowledge/company-info.mdを参照して業界特化の分析を実行してください")
    print("3. STEP1から順番に作業を進めてください")
    print("4. 前のSTEPの結果を次のSTEPで参照してください")
    print()
    print("クイックスタート:")
    print("@prompts/generic-quick-start.md をCursorで実行してください")
    print()

if __name__ == "__main__":
    main() 