#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
和光葬儀社プロジェクト自動セットアップスクリプト

新しい日付ディレクトリを作成し、テンプレートファイルをコピーして、
TODOマーカーを更新します。

使用方法:
    python workflows/setup-project.py                    # 今日の日付で作成
    python workflows/setup-project.py --date 20250625    # 指定日付で作成
"""

import os
import sys
import shutil
import argparse
from datetime import datetime
import re

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
    """テンプレートファイルをコピー"""
    template_dir = "outputs/templates"
    
    if not os.path.exists(template_dir):
        print(f"❌ エラー: テンプレートディレクトリ {template_dir} が見つかりません。")
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

def update_todo_markers(project_dir, current_datetime):
    """TODOマーカーを実行日時に更新"""
    updated_files = []
    
    for filename in os.listdir(project_dir):
        if filename.endswith('.md'):
            file_path = os.path.join(project_dir, filename)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 旧形式のTODOマーカーを更新
                old_pattern = r'TODO:\s*実行日時を記載'
                # 新形式のHTMLコメント形式TODOマーカーを更新
                new_pattern = r'<!-- TODO_EXECUTION_DATE -->\s*実行日時を記載\s*<!-- /TODO_EXECUTION_DATE -->'
                
                original_content = content
                
                # 旧形式の置換
                content = re.sub(old_pattern, current_datetime, content)
                # 新形式の置換
                content = re.sub(new_pattern, f'<!-- TODO_EXECUTION_DATE -->\n{current_datetime}\n<!-- /TODO_EXECUTION_DATE -->', content)
                
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    updated_files.append(filename)
                    print(f"✅ TODO更新: {filename}")
                
            except Exception as e:
                print(f"⚠️  警告: {filename} の更新中にエラーが発生しました: {e}")
    
    return updated_files

def create_project_readme(project_dir, date_str, current_datetime):
    """プロジェクト用README.mdを作成"""
    readme_content = f"""# 和光葬儀社プロジェクト - {date_str}

## プロジェクト情報
- **開始日**: {current_datetime}
- **プロジェクトディレクトリ**: `{project_dir}/`

## 作業ファイル
1. `01_competitor-analysis.md` - 競合分析レポート
2. `02_seo-analysis.md` - SEO分析・改善提案
3. `03_marketing-strategy.md` - マーケティング戦略立案
4. `04_lp-requirements.md` - LP要件定義
5. `05_lp-completion-report.md` - LP完成レポート

## 作業手順
1. 各ファイルの `<!-- TODO_XXX -->` マーカーを探す
2. マーカーで囲まれた部分を実際の内容に置き換える
3. 前のSTEPの結果を次のSTEPで参照する
4. 最終的にすべてのTODOマーカーを実際の内容に更新する

## 注意事項
- TODOマーカーは `<!-- TODO_XXX -->` と `<!-- /TODO_XXX -->` で囲まれています
- AIエージェントが自動的にこれらのマーカーを検索・置換できます
- 手動で編集する場合は、マーカーごと削除して実際の内容に置き換えてください

---
*このファイルは自動生成されました（{current_datetime}）*
"""
    
    readme_path = os.path.join(project_dir, 'README.md')
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"✅ プロジェクトREADME作成: README.md")

def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(
        description='和光葬儀社プロジェクトの自動セットアップ',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  python workflows/setup-project.py                    # 今日の日付で作成
  python workflows/setup-project.py --date 20250625    # 指定日付で作成
        """
    )
    parser.add_argument('--date', help='プロジェクト日付（YYYYMMDD形式）')
    
    args = parser.parse_args()
    
    print("🚀 和光葬儀社プロジェクト自動セットアップを開始します...")
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
    updated_files = update_todo_markers(project_dir, current_datetime)
    
    # 5. プロジェクトREADME作成
    create_project_readme(project_dir, target_date, current_datetime)
    
    print()
    print("✨ セットアップ完了！")
    print(f"📁 作業ディレクトリ: {project_dir}")
    print(f"📄 コピーされたファイル: {len(copied_files)}個")
    print(f"🔄 更新されたファイル: {len(updated_files)}個")
    print()
    print("📋 次のステップ:")
    print("1. 各ファイルの <!-- TODO_XXX --> マーカーを実際の内容に置き換えてください")
    print("2. STEP1から順番に作業を進めてください")
    print("3. 前のSTEPの結果を次のSTEPで参照してください")
    print()

if __name__ == "__main__":
    main() 