#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SerpAPI テスト用スクリプト（最小限のリクエスト）
"""

import requests
import json
from datetime import datetime
import os
import argparse
from dotenv import load_dotenv

# .envファイルから環境変数を読み込み
load_dotenv()

def test_serpapi(cli_api_key=None):
    """SerpAPIの動作テスト（1キーワードのみ）"""
    
    print("🧪 SerpAPI 動作テスト開始")
    print("=" * 40)
    
    # APIキー確認
    api_key = (cli_api_key or os.getenv("SERPAPI_KEY") or "").strip()
    if not api_key:
        print("❌ エラー: .envファイルのSERPAPI_KEYが設定されていません")
        print("📝 env-template.txt を .env にコピーして、APIキーを設定してください")
        return False
    
    print(f"🔑 APIキー確認: {api_key[:10]}..." if len(api_key) > 10 else api_key)
    
    # テスト用キーワード（1個のみ）
    test_keyword = "葬儀 横浜"
    location = os.getenv("TARGET_LOCATION", "Yokohama, Kanagawa, Japan")
    
    print(f"🔍 テストキーワード: {test_keyword}")
    print(f"📍 対象地域: {location}")
    print("⏰ API呼び出し中...")
    
    # API呼び出し
    params = {
        "engine": "google",
        "q": test_keyword,
        "location": location,
        "hl": "ja",
        "gl": "jp",
        "api_key": api_key
    }
    
    try:
        response = requests.get("https://serpapi.com/search", params=params)
        
        if response.status_code == 200:
            data = response.json()
            
            print("✅ API呼び出し成功！")
            print("\n📊 結果サマリー:")
            
            # 基本情報
            if "organic_results" in data:
                print(f"  🌐 オーガニック結果数: {len(data['organic_results'])}件")
                
                # 上位3サイトを表示
                print("  🥇 上位3サイト:")
                for i, result in enumerate(data["organic_results"][:3]):
                    title = result.get("title", "")[:40] + "..." if len(result.get("title", "")) > 40 else result.get("title", "")
                    print(f"    {i+1}位: {title}")
                
                # 和光葬儀社の順位チェック
                wako_rank = "圏外"
                for i, result in enumerate(data["organic_results"]):
                    if "wakousougisya.com" in result.get("link", "").lower():
                        wako_rank = f"{i+1}位"
                        break
                print(f"  🎯 和光葬儀社の順位: {wako_rank}")
            
            # 広告情報
            if "ads" in data and len(data["ads"]) > 0:
                print(f"  📢 広告数: {len(data['ads'])}件")
            else:
                print("  📢 広告: なし")
            
            # 関連検索
            if "related_searches" in data:
                related = [item.get("query", "") for item in data["related_searches"][:3]]
                print(f"  🔗 関連検索: {', '.join(related)}")
            
            # APIクレジット情報
            if "credits_left" in data.get("search_metadata", {}):
                credits = data["search_metadata"]["credits_left"]
                print(f"\n💳 残りクレジット: {credits}")
            
            # テスト結果保存
            save_test_result(test_keyword, data)
            
            print("\n🎉 テスト完了！")
            print("📝 詳細結果はtest-result.jsonを確認してください")
            return True
            
        else:
            print(f"❌ APIエラー: {response.status_code}")
            print(f"レスポンス: {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ エラー発生: {e}")
        return False

def save_test_result(keyword, data):
    """テスト結果を保存"""
    result = {
        "テスト日時": datetime.now().strftime("%Y年%m月%d日 %H:%M:%S"),
        "テストキーワード": keyword,
        "API呼び出し成功": True,
        "オーガニック結果数": len(data.get("organic_results", [])),
        "広告数": len(data.get("ads", [])),
        "詳細データ": data
    }
    
    try:
        os.makedirs("../outputs", exist_ok=True)
        with open("../outputs/test-result.json", 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"⚠️ ファイル保存エラー: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SerpAPI テストツール")
    parser.add_argument("--api-key", dest="api_key", help="SerpAPIのAPIキー（環境変数の代替）")
    parser.add_argument("--no-pause", action="store_true", help="終了時に一時停止しない")
    args = parser.parse_args()

    print("🚀 SerpAPI テストツール")
    print("📡 APIリクエスト: 1回のみ（最小限）")
    print("")

    success = test_serpapi(cli_api_key=args.api_key)

    if success:
        print("\n✅ .envファイルの設定とSerpAPIの接続が正常です！")
        print("📋 次のステップ:")
        print("  • 本格的な分析: python seo-keyword-analyzer.py")
        print("  • 8キーワード分析で合計8回のAPI呼び出し")
    else:
        print("\n❌ 設定に問題があります")
        print("📝 create-env-guide.md を参照して設定を確認してください")

    print("\n" + "=" * 40)
    if not args.no_pause:
        input("Enterキーで終了...")