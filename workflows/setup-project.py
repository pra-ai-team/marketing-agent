#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
汎用マーケティングツール プロジェクト自動セットアップスクリプト

設定ファイル（project-config.yaml）から企業・業界情報を読み込み、
動的にプロジェクトを作成します。

使用方法:
    python workflows/generic-setup-project.py                    # 今日の日付で作成
    python workflows/generic-setup-project.py --date 20250625    # 指定日付で作成
    python workflows/generic-setup-project.py --config custom.yaml  # 設定ファイル指定
"""

import os
import sys
import shutil
import argparse
from datetime import datetime
import re

# 設定ローダーをインポート
try:
    from config_loader import ConfigLoader
except ImportError:
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

def create_project_directory(date_str):
    """プロジェクトディレクトリを作成"""
    project_dir = f"outputs/{date_str}"
    
    if os.path.exists(project_dir):
        print(f"⚠️  警告: ディレクトリ {project_dir} は既に存在します。")
        response = input("続行しますか？ (y/n): ")
        if response.lower() != 'y':
            print("❌ 処理を中止しました。")
            sys.exit(1)
    else:
        os.makedirs(project_dir)
        print(f"✅ ディレクトリ作成: {project_dir}")
    
    return project_dir

def copy_template_files(project_dir):
    """汎用テンプレートファイルをコピー"""
    template_dir = "templates/generic"
    
    # 汎用テンプレートが存在しない場合は従来のテンプレートを使用
    if not os.path.exists(template_dir):
        template_dir = "outputs/templates"
        print(f"⚠️  汎用テンプレートが見つかりません。従来のテンプレートを使用します: {template_dir}")
    
    if not os.path.exists(template_dir):
        print(f"❌ エラー: テンプレートディレクトリが見つかりません: {template_dir}")
        sys.exit(1)
    
    copied_files = []
    for filename in os.listdir(template_dir):
        if filename.endswith('.md'):
            src_path = os.path.join(template_dir, filename)
            dst_path = os.path.join(project_dir, filename)
            shutil.copy2(src_path, dst_path)
            copied_files.append(filename)
            print(f"✅ ファイルコピー: {filename}")
    
    return copied_files

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
                
                # 基本的なTODOマーカーの更新
                replacements = {
                    # 実行日時
                    r'<!-- TODO_EXECUTION_DATE -->\s*実行日時を記載\s*<!-- /TODO_EXECUTION_DATE -->': f'<!-- TODO_EXECUTION_DATE -->\n{current_datetime}\n<!-- /TODO_EXECUTION_DATE -->',
                    r'TODO:\s*実行日時を記載': current_datetime,
                    
                    # 企業名の置換
                    r'和光葬儀社': company_name,
                    r'株式会社和光商事：和光葬儀社': company_name,
                    r'TARGET_COMPANY': company_name,
                    
                    # 業界の置換
                    r'葬儀業界': industry,
                    r'葬儀サービス業': industry,
                    r'TARGET_INDUSTRY': industry,
                    
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
                    print(f"✅ TODO更新: {filename}")
                
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
    
    print(f"✅ 動的知識ベース作成: knowledge/company-info.md")
    
    # 設定サマリーファイル
    summary_content = config_loader.generate_project_summary()
    summary_file = os.path.join(project_dir, 'project-summary.md')
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary_content)
    
    print(f"✅ プロジェクトサマリー作成: project-summary.md")

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
- **企業情報**: `config/project-config.yaml`の company セクション
- **業界情報**: `config/project-config.yaml`の industry セクション
- **競合情報**: `config/project-config.yaml`の competitors セクション
- **SEO設定**: `config/project-config.yaml`の seo セクション

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
    
    print(f"✅ プロジェクトREADME作成: README.md")

def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(
        description='汎用マーケティングツール プロジェクト自動セットアップ',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  python workflows/generic-setup-project.py                    # 今日の日付で作成
  python workflows/generic-setup-project.py --date 20250625    # 指定日付で作成
  python workflows/generic-setup-project.py --config custom.yaml  # 設定ファイル指定
        """
    )
    parser.add_argument('--date', help='プロジェクト日付（YYYYMMDD形式）')
    parser.add_argument('--config', help='設定ファイルパス（デフォルト: config/project-config.yaml）')
    
    args = parser.parse_args()
    
    print("🚀 汎用マーケティングツール プロジェクト自動セットアップを開始します...")
    print()
    
    # 設定ファイルの読み込み
    try:
        config_loader = ConfigLoader(args.config)
        print("✅ 設定ファイル読み込み完了")
    except Exception as e:
        print(f"❌ 設定ファイル読み込みエラー: {e}")
        sys.exit(1)
    
    # 設定の妥当性チェック
    errors, warnings = config_loader.validate_config()
    if errors:
        print("❌ 設定エラーが見つかりました:")
        for error in errors:
            print(f"  - {error}")
        print("config/project-config.yamlを修正してから再実行してください。")
        sys.exit(1)
    
    if warnings:
        print("⚠️  設定警告:")
        for warning in warnings:
            print(f"  - {warning}")
        print()
    
    # 設定サマリーの表示
    config_loader.print_config_summary()
    print()
    
    # 1. 日付の決定
    target_date = get_target_date(args.date)
    current_datetime = get_current_datetime()
    
    print(f"📅 対象日付: {target_date}")
    print(f"🕐 実行日時: {current_datetime}")
    print()
    
    # 2. プロジェクトディレクトリ作成
    project_dir = create_project_directory(target_date)
    
    # 3. テンプレートファイルコピー
    copied_files = copy_template_files(project_dir)
    
    # 4. TODOマーカー更新
    updated_files = update_todo_markers(project_dir, current_datetime, config_loader)
    
    # 5. 動的知識ベース作成
    create_dynamic_knowledge_base(project_dir, config_loader)
    
    # 6. プロジェクトREADME作成
    create_project_readme(project_dir, target_date, current_datetime, config_loader)
    
    print()
    print("✨ セットアップ完了！")
    print(f"📁 作業ディレクトリ: {project_dir}")
    print(f"📄 コピーされたファイル: {len(copied_files)}個")
    print(f"🔄 更新されたファイル: {len(updated_files)}個")
    print()
    print("📋 次のステップ:")
    print("1. 各ファイルの <!-- TODO_XXX --> マーカーを実際の内容に置き換えてください")
    print("2. knowledge/company-info.mdを参照して業界特化の分析を実行してください")
    print("3. STEP1から順番に作業を進めてください")
    print("4. 前のSTEPの結果を次のSTEPで参照してください")
    print()
    print("🎯 クイックスタート:")
    print("@prompts/generic-quick-start.md をCursorで実行してください")
    print()

if __name__ == "__main__":
    main() 