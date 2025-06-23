#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SerpAPI 簡易テストスクリプト（.envファイル不使用）
"""

import requests
import json
from datetime import datetime
import os

def test_serpapi_simple():
    """SerpAPIの動作テスト（環境変数から直接読み取り）"""
    
    print("🧪 SerpAPI 簡易テスト開始")
    print("=" * 40)
    
    # 環境変数から直接APIキーを取得
    api_key = os.environ.get("SERPAPI_KEY")
    
    # .envファイルが読めない場合は手動設定を促す
    if not api_key or api_key == "your_serpapi_key_here":
        print("❌ エラー: APIキーが設定されていません")
        print("\n🔧 手動設定方法:")
        print("以下のコマンドでAPIキーを設定してください:")
        print('$env:SERPAPI_KEY="あなたの実際のAPIキー"')
        print("\nまたは:")
        api_key = input("APIキーを直接入力してください: ").strip()
        if not api_key:
            print("❌ APIキーが入力されませんでした")
            return False
    
    print(f"🔑 APIキー確認: {api_key[:10]}..." if len(api_key) > 10 else f"🔑 APIキー確認: {api_key}")
    
    # テスト用キーワード（1個のみ）
    test_keyword = "葬儀 横浜"
    location = "Yokohama, Kanagawa, Japan"  # 英語の地域名に変更
    
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
            if "search_metadata" in data and "credits_left" in data["search_metadata"]:
                credits = data["search_metadata"]["credits_left"]
                print(f"\n💳 残りクレジット: {credits}")
            
            # テスト結果保存
            save_test_result(test_keyword, data)
            
            print("\n🎉 テスト完了！")
            return True
            
        else:
            print(f"❌ APIエラー: {response.status_code}")
            error_data = response.text[:200] if response.text else "レスポンスなし"
            print(f"レスポンス: {error_data}...")
            
            if response.status_code == 401:
                print("\n💡 解決方法:")
                print("1. SerpAPIアカウントが作成されているか確認")
                print("2. APIキーが正しいか確認")
                print("3. https://serpapi.com/manage-api-key でキーを再確認")
            
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
        with open("../outputs/simple-test-result.json", 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print("💾 結果を simple-test-result.json に保存しました")
    except Exception as e:
        print(f"⚠️ ファイル保存エラー: {e}")

if __name__ == "__main__":
    print("🚀 SerpAPI 簡易テストツール")
    print("📡 APIリクエスト: 1回のみ（最小限）")
    print("🔧 .envファイル不使用版")
    print("")
    
    success = test_serpapi_simple()
    
    if success:
        print("\n✅ SerpAPIの接続が正常です！")
        print("📋 次のステップ:")
        print("  • 本格的な分析を実行する場合")
        print("  • 8キーワード分析で合計8回のAPI呼び出し")
    else:
        print("\n❌ 設定に問題があります")
        print("📝 上記の解決方法を参照してください")
    
    print("\n" + "=" * 40)
    input("Enterキーで終了...") 