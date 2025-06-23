#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
プロジェクト進捗確認スクリプト

TODOマーカーの残存確認と完了率計算を自動化
"""

import os
import glob
import re
import json
from datetime import datetime
from pathlib import Path

def find_latest_project():
    """最新のプロジェクトディレクトリを取得"""
    outputs_dir = Path("outputs")
    if not outputs_dir.exists():
        return None
    
    project_dirs = [d for d in outputs_dir.iterdir() 
                    if d.is_dir() and d.name.isdigit() and len(d.name) == 8]
    
    if not project_dirs:
        return None
    
    return max(project_dirs, key=lambda x: x.name)

def count_todo_markers(file_path):
    """ファイル内のTODOマーカー数をカウント"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # HTMLコメント形式のTODOマーカーを検索
        html_todos = re.findall(r'<!-- TODO_\w+ -->', content)
        # 旧形式のTODOマーカーを検索  
        legacy_todos = re.findall(r'TODO:', content)
        
        return len(html_todos) + len(legacy_todos), html_todos, legacy_todos
    
    except Exception as e:
        print(f"⚠️ ファイル読み込みエラー: {file_path} - {e}")
        return 0, [], []

def generate_progress_report(project_dir):
    """進捗レポートを生成"""
    report = {
        "project_dir": str(project_dir),
        "check_time": datetime.now().isoformat(),
        "files": {},
        "summary": {}
    }
    
    md_files = list(project_dir.glob("*.md"))
    if not md_files:
        return report
    
    total_todos = 0
    
    for file_path in md_files:
        filename = file_path.name
        if filename == "README.md":  # プロジェクトREADMEは除外
            continue
            
        todo_count, html_todos, legacy_todos = count_todo_markers(file_path)
        
        file_info = {
            "remaining_todos": todo_count,
            "html_todos": html_todos,
            "legacy_todos": legacy_todos,
            "is_complete": todo_count == 0
        }
        
        report["files"][filename] = file_info
        total_todos += todo_count
    
    # サマリー情報
    completed_files = sum(1 for info in report["files"].values() if info["is_complete"])
    total_files = len(report["files"])
    
    report["summary"] = {
        "total_files": total_files,
        "completed_files": completed_files,
        "completion_rate": round((completed_files / total_files * 100) if total_files > 0 else 100, 2),
        "total_remaining_todos": total_todos
    }
    
    return report

def print_progress_report(report):
    """進捗レポートを見やすく表示"""
    print("📊 プロジェクト進捗レポート")
    print("=" * 50)
    print(f"📁 プロジェクト: {report['project_dir']}")
    print(f"🕐 確認時刻: {report['check_time']}")
    print()
    
    summary = report["summary"]
    print("📈 全体サマリー")
    print("-" * 30)
    print(f"完了ファイル数: {summary['completed_files']}/{summary['total_files']}")
    print(f"全体完了率: {summary['completion_rate']:.1f}%")
    print(f"残りTODO: {summary['total_remaining_todos']}個")
    print()
    
    if summary["total_remaining_todos"] == 0:
        print("🎉 すべてのTODOマーカーが完了しました！")
    else:
        print("📋 ファイル別進捗")
        print("-" * 30)
        
        for filename, info in report["files"].items():
            status_icon = "✅" if info["is_complete"] else "🔄"
            print(f"{status_icon} {filename}")
            
            if info["remaining_todos"] > 0:
                print(f"   残りTODO: {info['remaining_todos']}個")
                if info["html_todos"]:
                    print(f"     HTML形式: {', '.join(info['html_todos'])}")
                if info["legacy_todos"]:
                    print(f"     旧形式: {len(info['legacy_todos'])}個")
            print()

def main():
    """メイン処理"""
    print("🔍 プロジェクト進捗を確認しています...")
    print()
    
    # 最新プロジェクトディレクトリを取得
    project_dir = find_latest_project()
    
    if not project_dir:
        print("❌ エラー: outputs/ ディレクトリにプロジェクトが見つかりません")
        print("python workflows/setup-project.py でプロジェクトを作成してください")
        return
    
    print(f"📁 対象プロジェクト: {project_dir}")
    print()
    
    # 進捗レポート生成
    report = generate_progress_report(project_dir)
    
    # レポート表示
    print_progress_report(report)
    
    # LP関連ファイルの確認
    lp_dir = project_dir / "lp-files"
    if lp_dir.exists():
        lp_files = list(lp_dir.glob("*.html")) + list(lp_dir.glob("*.css")) + list(lp_dir.glob("*.js"))
        print(f"🎨 LP関連ファイル: {len(lp_files)}個")
        for lp_file in lp_files:
            print(f"   📄 {lp_file.name}")
    else:
        print("🎨 LP関連ファイル: 未作成")
    
    print()
    print("💡 次のステップ:")
    if report["summary"]["total_remaining_todos"] > 0:
        print("- 残りのTODOマーカーを実際の内容に更新してください")
        print("- 前のSTEPの結果を参照して次のSTEPを進めてください")
    else:
        print("- 🎉 プロジェクト完了！品質確認を実行してください")
        print("- LP関連ファイルの動作確認を行ってください")

if __name__ == "__main__":
    main() 