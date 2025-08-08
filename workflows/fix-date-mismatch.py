#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日付不一致修正ツール

プロジェクトフォルダ名と実行日時記録の不一致を検出・修正
"""

import os
import sys
import shutil
import re
import argparse
from datetime import datetime
from pathlib import Path

def scan_date_mismatches():
    """日付不一致を検出"""
    outputs_dir = Path("outputs")
    if not outputs_dir.exists():
        print("❌ outputs/ ディレクトリが見つかりません")
        return []
    
    mismatches = []
    
    for project_dir in outputs_dir.iterdir():
        if not project_dir.is_dir() or not project_dir.name.isdigit() or len(project_dir.name) != 8:
            continue
            
        folder_date = project_dir.name
        
        # 各ファイルの実行日時をチェック
        for md_file in project_dir.glob("*.md"):
            if md_file.name == "README.md":
                continue
                
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # TODO_EXECUTION_DATE マーカーから日時抽出
                date_match = re.search(r'<!-- TODO_EXECUTION_DATE -->\s*(\d{4}年\d{2}月\d{2}日 \d{2}:\d{2}:\d{2})\s*<!-- /TODO_EXECUTION_DATE -->', content)
                
                if date_match:
                    execution_datetime = date_match.group(1)
                    # 日付部分のみ抽出 (YYYY年MM月DD日)
                    date_only_match = re.match(r'(\d{4})年(\d{2})月(\d{2})日', execution_datetime)
                    if date_only_match:
                        year, month, day = date_only_match.groups()
                        execution_date = f"{year}{month}{day}"
                        
                        if folder_date != execution_date:
                            mismatches.append({
                                "project_dir": str(project_dir),
                                "folder_date": folder_date,
                                "execution_date": execution_date,
                                "execution_datetime": execution_datetime,
                                "file": str(md_file)
                            })
                            break  # 1つのファイルで見つかれば十分
                        
            except Exception as e:
                print(f"⚠️ {md_file} 読み込みエラー: {e}")
    
    return mismatches

def display_mismatches(mismatches):
    """不一致を表示"""
    if not mismatches:
        print("✅ 日付不一致は見つかりませんでした")
        return False
    
    print("🚨 日付不一致を検出しました:")
    print("=" * 60)
    
    for i, mismatch in enumerate(mismatches, 1):
        print(f"{i}. プロジェクト: {mismatch['project_dir']}")
        print(f"   フォルダ日付: {mismatch['folder_date']}")
        print(f"   実行日時: {mismatch['execution_datetime']}")
        print(f"   実行日付: {mismatch['execution_date']}")
        print()
    
    return True

def fix_mismatch(mismatch, method):
    """不一致を修正"""
    project_path = Path(mismatch['project_dir'])
    folder_date = mismatch['folder_date']
    execution_date = mismatch['execution_date']
    
    if method == "rename_folder":
        # フォルダ名を実行日付に変更
        new_folder_name = f"outputs/{execution_date}"
        new_path = Path(new_folder_name)
        
        if new_path.exists():
            print(f"❌ 移動先 {new_folder_name} は既に存在します")
            return False
        
        try:
            shutil.move(str(project_path), str(new_path))
            print(f"✅ フォルダ名変更: {project_path} → {new_path}")
            return True
        except Exception as e:
            print(f"❌ フォルダ名変更エラー: {e}")
            return False
    
    elif method == "update_files":
        # ファイル内の実行日時をフォルダ日付に更新
        folder_datetime = datetime.strptime(folder_date, '%Y%m%d').strftime('%Y年%m月%d日 %H:%M:%S')
        
        updated_files = 0
        for md_file in project_path.glob("*.md"):
            if md_file.name == "README.md":
                continue
            
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # TODO_EXECUTION_DATE マーカーを更新
                pattern = r'(<!-- TODO_EXECUTION_DATE -->\s*)(\d{4}年\d{2}月\d{2}日 \d{2}:\d{2}:\d{2})(\s*<!-- /TODO_EXECUTION_DATE -->)'
                new_content = re.sub(pattern, f'\\1{folder_datetime}\\3', content)
                
                if new_content != content:
                    with open(md_file, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    updated_files += 1
                    
            except Exception as e:
                print(f"⚠️ {md_file} 更新エラー: {e}")
        
        print(f"✅ {updated_files}個のファイルを更新しました")
        return updated_files > 0

def main():
    """メイン処理"""
    print("🔧 日付不一致修正ツール")
    print("=" * 40)
    
    parser = argparse.ArgumentParser(description="日付不一致修正ツール")
    parser.add_argument("--method", choices=["rename_folder", "update_files"], help="修正方法を指定")
    parser.add_argument("--yes", action="store_true", help="確認なしで実行")
    args = parser.parse_args()

    # 不一致を検出
    mismatches = scan_date_mismatches()
    
    if not display_mismatches(mismatches):
        return

    method = args.method
    if not method:
        print("🛠️ 修正方法を選択してください:")
        print("1. フォルダ名を実行日付に変更")
        print("2. ファイル内の実行日時をフォルダ日付に更新")
        print("3. 何もしない")
        try:
            choice = input("\n選択 (1-3): ").strip()
        except KeyboardInterrupt:
            print("\n🚫 修正が中断されました")
            return
        if choice == "1":
            method = "rename_folder"
        elif choice == "2":
            method = "update_files"
        else:
            print("❌ 修正をキャンセルしました")
            return

    if not args.yes and args.method:
        confirm = input(f"実行確認: method={method} で実行します。よろしいですか？ (y/n): ").strip().lower()
        if confirm != "y":
            print("❌ 実行をキャンセルしました")
            return

    # 各不一致を修正
    for mismatch in mismatches:
        print(f"\n🔧 修正中: {mismatch['project_dir']}")
        fix_mismatch(mismatch, method)
        
    print("\n✨ 修正完了！")

if __name__ == "__main__":
    main() 