#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
システム日時確認ユーティリティ

システムの日付・時刻設定を詳細に確認し、
日付関連の問題をデバッグするためのツール
"""

import sys
import time
import platform
from datetime import datetime, timezone
import subprocess

def check_system_datetime():
    """システム日時の詳細確認"""
    print("🔍 システム日時診断ツール")
    print("=" * 50)
    
    # Python での日時取得
    py_now = datetime.now()
    py_utc = datetime.now(timezone.utc)
    
    print("📅 Python datetime 情報:")
    print(f"   ローカル時刻: {py_now}")
    print(f"   UTC時刻: {py_utc}")
    print(f"   タイムゾーン: {py_now.astimezone().tzinfo}")
    print(f"   フォーマット済み: {py_now.strftime('%Y%m%d')}")
    print()
    
    # システム情報
    print("💻 システム情報:")
    print(f"   OS: {platform.system()} {platform.release()}")
    print(f"   Python版: {platform.python_version()}")
    print(f"   マシン: {platform.machine()}")
    print()
    
    # Windows固有の時刻確認
    if platform.system() == "Windows":
        print("🪟 Windows システム時刻:")
        try:
            # PowerShellで日時取得
            result = subprocess.run([
                "powershell", "-Command", "Get-Date -Format 'yyyy/MM/dd HH:mm:ss'"
            ], capture_output=True, text=True, encoding='utf-8')
            
            if result.returncode == 0:
                win_datetime = result.stdout.strip()
                print(f"   PowerShell: {win_datetime}")
            else:
                print(f"   PowerShell取得エラー: {result.stderr}")
            
            # タイムゾーン情報取得
            tz_result = subprocess.run([
                "powershell", "-Command", "Get-TimeZone | Select-Object Id, DisplayName"
            ], capture_output=True, text=True, encoding='utf-8')
            
            if tz_result.returncode == 0:
                print("   タイムゾーン:")
                for line in tz_result.stdout.strip().split('\n')[2:]:  # ヘッダー行をスキップ
                    if line.strip():
                        print(f"     {line}")
            
        except Exception as e:
            print(f"   Windows時刻取得エラー: {e}")
    
    print()
    
    # 異常値チェック
    current_year = py_now.year
    print("⚠️  日付妥当性チェック:")
    
    # より現実的な範囲チェック
    if current_year >= 2030:
        print(f"   🚨 警告: 年が {current_year} です（異常に未来）")
        print("   → システム時計の設定を確認してください")
    elif current_year <= 2020:
        print(f"   🚨 警告: 年が {current_year} です（古すぎます）")
        print("   → システム時計の設定を確認してください")
    else:
        print("   ✅ 年は妥当範囲内です")
    
    # 月・日の基本チェック
    if py_now.month < 1 or py_now.month > 12:
        print(f"   🚨 異常: 月が {py_now.month} です")
    elif py_now.day < 1 or py_now.day > 31:
        print(f"   🚨 異常: 日が {py_now.day} です")
    else:
        print("   ✅ 月・日は妥当範囲内です")
    
    print()
    
    # 推奨対処法
    print("🛠️  推奨対処法:")
    print("1. Windowsの「設定」→「時刻と言語」→「日付と時刻」を確認")
    print("2. 「時刻を自動的に設定する」を有効にする")
    print("3. 手動で正しい日付を設定する")
    print("4. プロジェクト作成時に --date オプションで正しい日付を指定")
    
    # 実際の日付入力提案
    print()
    suggested_date = py_now.strftime('%Y%m%d')
    print(f"💡 今日の日付でプロジェクト作成:")
    print(f"   python workflows/setup-project.py --date {suggested_date}")

def main():
    """メイン処理"""
    try:
        check_system_datetime()
    except KeyboardInterrupt:
        print("\n🚫 診断が中断されました")
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")

if __name__ == "__main__":
    main() 