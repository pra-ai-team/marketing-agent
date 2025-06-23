#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
和光葬儀社 SEOキーワード分析ツール（動的SERP分析版）
SerpAPI（無料プラン）を使用してリアルタイム検索結果分析を実行

作成日: 2025年1月27日
更新日: 2025年1月27日
機能: 競合SERP分析、キーワード機会発見、動的データ取得
"""

import requests
import json
import time
from datetime import datetime
import os
from dotenv import load_dotenv
from urllib.parse import urlparse
import re

# .envファイルから環境変数を読み込み
load_dotenv()

class FuneralSEOAnalyzer:
    def __init__(self, api_key):
        """
        SerpAPI（無料プラン）を使用した葬儀業界SEOキーワード分析クラス
        動的SERP分析・競合分析機能付き
        """
        self.api_key = api_key
        self.base_url = "https://serpapi.com/search"
        self.target_location = os.getenv("TARGET_LOCATION", "神奈川県横浜市")
        self.company_domain = os.getenv("COMPANY_DOMAIN", "wakousougisya.com")
        
        # 競合ドメインのパターン（葬儀業界主要プレイヤー）
        self.competitor_patterns = {
            "大手チェーン": ["aeon-life.jp", "koekisha.co.jp", "e-sogi.com", "sougi-sos.com"],
            "地域密着": ["yokohama", "kanagawa", "sougi"],
            "比較ポータル": ["iisogi.com", "chiisanaososhiki.jp", "osohshiki.jp", "sogi.jp"],
            "情報サイト": ["syukatsulabo.jp", "osohshiki-plaza.com", "sougi-guide"]
        }
        
    def get_search_results(self, keyword, location=None):
        """指定キーワードの検索結果を詳細取得"""
        if location is None:
            location = self.target_location
            
        params = {
            "engine": "google",
            "q": keyword,
            "location": location,
            "hl": "ja",
            "gl": "jp",
            "api_key": self.api_key,
            "num": 100  # より多くの結果を取得
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"  ⚠️ APIエラー: {response.status_code}")
                return None
        except Exception as e:
            print(f"  ❌ エラー: {keyword}の検索結果取得に失敗 - {e}")
            return None
    
    def analyze_funeral_keywords_dynamic(self):
        """和光葬儀社向け動的キーワード分析実行"""
        
        # 拡張されたターゲットキーワード（プロンプト準拠）
        target_keywords = {
            "メイン（優先度：高）": [
                "葬儀 横浜",
                "家族葬 神奈川", 
                "葬儀社 横浜",
                "直葬 費用"
            ],
            "地域特化（優先度：中）": [
                "葬儀 港北区",
                "葬儀社 神奈川区",
                "火葬式 横浜"
            ],
            "差別化（優先度：中）": [
                "葬儀 追加料金なし 横浜",
                "24時間対応 葬儀社 神奈川",
                "葬祭ディレクター 資格者 横浜"
            ]
        }
        
        all_keywords = []
        for category, keywords in target_keywords.items():
            all_keywords.extend(keywords)
        
        analysis_results = {
            "分析実行情報": {
                "分析日時": datetime.now().strftime("%Y年%m月%d日 %H:%M:%S"),
                "対象地域": self.target_location,
                "分析対象企業": "和光葬儀社",
                "使用API": "SerpAPI（動的分析版）",
                "分析キーワード数": len(all_keywords),
                "データ取得成功率": "0/0 (0%)"
            },
            "リアルタイム順位・競合分析": {
                "和光葬儀社順位状況": {},
                "競合SERP分析結果": {
                    "主要競合パターン": {},
                    "SERP機能分析": {}
                }
            },
            "動的発見キーワード機会": {
                "新規ターゲットキーワード": [],
                "コンテンツギャップ分析結果": {}
            },
            "詳細データ": {}
        }
        
        print("=" * 70)
        print("🔍 和光葬儀社 SEOキーワード動的分析開始")
        print("=" * 70)
        print(f"📅 分析日時: {analysis_results['分析実行情報']['分析日時']}")
        print(f"📍 対象地域: {analysis_results['分析実行情報']['対象地域']}")
        print(f"🎯 分析対象: {len(all_keywords)}キーワード（3カテゴリ）")
        print("📊 機能: 競合SERP分析、キーワード機会発見、SERP機能分析")
        print("=" * 70)
        
        successful_analyses = 0
        wako_found_count = 0
        all_related_keywords = set()
        competitor_analysis = {}
        serp_features = {"local_pack": 0, "ads": 0, "paa": 0, "knowledge_graph": 0}
        
        for category, keywords in target_keywords.items():
            print(f"\n📋 カテゴリ: {category}")
            print("-" * 50)
            
            for i, keyword in enumerate(keywords, 1):
                print(f"\n[{successful_analyses + 1}/{len(all_keywords)}] 🔍 分析中: {keyword}")
                
                # API制限回避のため待機
                if successful_analyses > 0:
                    time.sleep(3)
                
                serp_data = self.get_search_results(keyword)
                
                if serp_data:
                    # 詳細分析実行
                    keyword_analysis = self.extract_comprehensive_insights(keyword, serp_data)
                    analysis_results["詳細データ"][keyword] = keyword_analysis
                    
                    # 和光葬儀社順位記録
                    analysis_results["リアルタイム順位・競合分析"]["和光葬儀社順位状況"][keyword] = {
                        "順位": keyword_analysis["和光葬儀社の順位"],
                        "上位3サイト": keyword_analysis["上位競合サイト"][:3] if keyword_analysis["上位競合サイト"] else []
                    }
                    
                    # 関連キーワード収集
                    all_related_keywords.update(keyword_analysis["関連検索"])
                    
                    # 競合分析データ蓄積
                    self.accumulate_competitor_data(keyword_analysis, competitor_analysis)
                    
                    # SERP機能カウント
                    self.count_serp_features(keyword_analysis, serp_features)
                    
                    # 結果をリアルタイム表示
                    self.print_detailed_keyword_results(keyword, keyword_analysis)
                    successful_analyses += 1
                    
                    if keyword_analysis["和光葬儀社の順位"] != "圏外":
                        wako_found_count += 1
                else:
                    print(f"  ❌ {keyword}の分析に失敗しました")
        
        # 分析結果の統合・サマリー作成
        analysis_results["分析実行情報"]["データ取得成功率"] = f"{successful_analyses}/{len(all_keywords)} ({(successful_analyses/len(all_keywords)*100):.1f}%)"
        
        # 競合分析結果の整理
        analysis_results["リアルタイム順位・競合分析"]["競合SERP分析結果"] = {
            "主要競合パターン": self.analyze_competitor_patterns(competitor_analysis),
            "SERP機能分析": self.format_serp_features(serp_features, successful_analyses)
        }
        
        # 新規キーワード機会の分析
        analysis_results["動的発見キーワード機会"] = self.discover_keyword_opportunities(all_related_keywords, analysis_results["詳細データ"])
        
        # 結果をファイルに保存
        self.save_comprehensive_results(analysis_results)
        self.print_comprehensive_summary(analysis_results)
        
        return analysis_results
    
    def extract_comprehensive_insights(self, keyword, serp_data):
        """検索結果から包括的なインサイトを抽出（SERP機能分析含む）"""
        insights = {
            "競合サイト数": 0,
            "上位競合サイト": [],
            "関連検索": [],
            "広告出稿状況": "無し",
            "和光葬儀社の順位": "圏外",
            "検索結果の特徴": [],
            "SERP機能": {
                "local_pack": False,
                "ads_count": 0,
                "paa_questions": [],
                "knowledge_graph": False,
                "featured_snippet": False
            },
            "競合分類": {"大手チェーン": 0, "地域密着": 0, "比較ポータル": 0, "情報サイト": 0, "その他": 0}
        }
        
        # オーガニック検索結果の詳細分析
        if "organic_results" in serp_data:
            insights["競合サイト数"] = len(serp_data["organic_results"])
            
            # 上位20サイトを詳細分析
            for i, result in enumerate(serp_data["organic_results"][:20]):
                site_info = {
                    "順位": i + 1,
                    "タイトル": result.get("title", ""),
                    "URL": result.get("link", ""),
                    "ドメイン": self.extract_domain(result.get("link", "")),
                    "スニペット": result.get("snippet", "")[:100] + "..." if result.get("snippet") else "",
                    "競合カテゴリ": self.classify_competitor(result.get("link", ""))
                }
                insights["上位競合サイト"].append(site_info)
                
                # 競合分類カウント
                category = site_info["競合カテゴリ"]
                insights["競合分類"][category] += 1
                
                # 和光葬儀社の順位チェック
                if self.company_domain in result.get("link", "").lower():
                    insights["和光葬儀社の順位"] = f"{i + 1}位"
        
        # 関連検索キーワード（拡張）
        if "related_searches" in serp_data:
            insights["関連検索"] = [
                item.get("query", "") for item in serp_data["related_searches"]
            ]
        
        # People Also Ask分析
        if "people_also_ask" in serp_data:
            insights["SERP機能"]["paa_questions"] = [
                paa.get("question", "") for paa in serp_data["people_also_ask"]
            ]
        
        # 広告の詳細分析
        if "ads" in serp_data and len(serp_data["ads"]) > 0:
            insights["広告出稿状況"] = f"{len(serp_data['ads'])}件の広告あり"
            insights["SERP機能"]["ads_count"] = len(serp_data["ads"])
        
        # ローカルパック
        if "local_results" in serp_data:
            insights["SERP機能"]["local_pack"] = True
            insights["検索結果の特徴"].append("ローカル検索結果あり")
        
        # ナレッジグラフ
        if "knowledge_graph" in serp_data:
            insights["SERP機能"]["knowledge_graph"] = True
            insights["検索結果の特徴"].append("ナレッジグラフあり")
        
        # 特集スニペット
        if "featured_snippet" in serp_data:
            insights["SERP機能"]["featured_snippet"] = True
            insights["検索結果の特徴"].append("特集スニペットあり")
        
        return insights
    
    def classify_competitor(self, url):
        """URLから競合カテゴリを分類"""
        if not url:
            return "その他"
        
        url_lower = url.lower()
        
        for pattern in self.competitor_patterns["大手チェーン"]:
            if pattern in url_lower:
                return "大手チェーン"
        
        for pattern in self.competitor_patterns["比較ポータル"]:
            if pattern in url_lower:
                return "比較ポータル"
        
        for pattern in self.competitor_patterns["地域密着"]:
            if pattern in url_lower:
                return "地域密着"
        
        for pattern in self.competitor_patterns["情報サイト"]:
            if pattern in url_lower:
                return "情報サイト"
        
        return "その他"
    
    def accumulate_competitor_data(self, keyword_analysis, competitor_analysis):
        """競合データを蓄積"""
        for site in keyword_analysis["上位競合サイト"][:10]:  # 上位10位まで
            domain = site["ドメイン"]
            if domain and self.company_domain not in domain:
                if domain not in competitor_analysis:
                    competitor_analysis[domain] = {
                        "出現回数": 0,
                        "平均順位": 0,
                        "順位リスト": [],
                        "カテゴリ": site["競合カテゴリ"],
                        "タイトルパターン": []
                    }
                
                competitor_analysis[domain]["出現回数"] += 1
                competitor_analysis[domain]["順位リスト"].append(site["順位"])
                competitor_analysis[domain]["タイトルパターン"].append(site["タイトル"][:50])
                competitor_analysis[domain]["平均順位"] = sum(competitor_analysis[domain]["順位リスト"]) / len(competitor_analysis[domain]["順位リスト"])
    
    def count_serp_features(self, keyword_analysis, serp_features):
        """SERP機能の出現をカウント"""
        if keyword_analysis["SERP機能"]["local_pack"]:
            serp_features["local_pack"] += 1
        if keyword_analysis["SERP機能"]["ads_count"] > 0:
            serp_features["ads"] += 1
        if keyword_analysis["SERP機能"]["paa_questions"]:
            serp_features["paa"] += 1
        if keyword_analysis["SERP機能"]["knowledge_graph"]:
            serp_features["knowledge_graph"] += 1
    
    def analyze_competitor_patterns(self, competitor_analysis):
        """競合パターンを分析"""
        # 出現回数順にソート
        sorted_competitors = sorted(
            competitor_analysis.items(), 
            key=lambda x: x[1]["出現回数"], 
            reverse=True
        )
        
        patterns = {}
        for domain, data in sorted_competitors[:10]:  # 上位10競合
            patterns[domain] = {
                "出現キーワード数": data["出現回数"],
                "平均順位": round(data["平均順位"], 1),
                "カテゴリ": data["カテゴリ"],
                "SEO戦略": self.analyze_title_patterns(data["タイトルパターン"])
            }
        
        return patterns
    
    def analyze_title_patterns(self, titles):
        """タイトルパターンからSEO戦略を分析"""
        if not titles:
            return "不明"
        
        # よく使われる言葉を抽出
        common_words = []
        for title in titles:
            words = re.findall(r'[一-龯ァ-ヶー]+', title)  # 日本語のみ抽出
            common_words.extend(words)
        
        # 頻出単語TOP3
        from collections import Counter
        word_counts = Counter(common_words)
        top_words = [word for word, count in word_counts.most_common(3)]
        
        return f"よく使用: {', '.join(top_words)}" if top_words else "パターン不明"
    
    def format_serp_features(self, serp_features, total_keywords):
        """SERP機能の分析結果をフォーマット"""
        if total_keywords == 0:
            return {"エラー": "分析データなし"}
        
        return {
            "ローカルパック表示": f"{serp_features['local_pack']}キーワード（{(serp_features['local_pack']/total_keywords*100):.1f}%）",
            "広告表示": f"{serp_features['ads']}キーワード（{(serp_features['ads']/total_keywords*100):.1f}%）",
            "PAA表示": f"{serp_features['paa']}キーワード（{(serp_features['paa']/total_keywords*100):.1f}%）",
            "ナレッジグラフ": f"{serp_features['knowledge_graph']}キーワード（{(serp_features['knowledge_graph']/total_keywords*100):.1f}%）"
        }
    
    def discover_keyword_opportunities(self, all_related_keywords, detailed_data):
        """キーワード機会を発見・分析"""
        # 関連キーワードから新規機会を特定
        existing_keywords = set(detailed_data.keys())
        new_opportunities = []
        
        for related_kw in all_related_keywords:
            if related_kw not in existing_keywords and related_kw:
                # 競合強度を推定（簡易版）
                strength = self.estimate_competition_strength(related_kw, detailed_data)
                new_opportunities.append({
                    "キーワード": related_kw,
                    "検索意図": self.infer_search_intent(related_kw),
                    "競合強度": strength
                })
        
        # 重要度順にソート
        new_opportunities.sort(key=lambda x: self.calculate_opportunity_score(x), reverse=True)
        
        # コンテンツギャップ分析
        content_gaps = self.analyze_content_gaps(detailed_data)
        
        return {
            "新規ターゲットキーワード": new_opportunities[:10],  # TOP10
            "コンテンツギャップ分析結果": content_gaps
        }
    
    def estimate_competition_strength(self, keyword, detailed_data):
        """キーワードの競合強度を推定"""
        # 類似キーワードから推定
        funeral_terms = ["葬儀", "家族葬", "直葬", "火葬"]
        if any(term in keyword for term in funeral_terms):
            return "中"
        elif "横浜" in keyword or "神奈川" in keyword:
            return "弱"
        else:
            return "強"
    
    def infer_search_intent(self, keyword):
        """検索意図を推測"""
        if "費用" in keyword or "料金" in keyword or "安い" in keyword:
            return "価格情報"
        elif "口コミ" in keyword or "評判" in keyword:
            return "評価・比較"
        elif "流れ" in keyword or "手続き" in keyword:
            return "情報収集"
        elif "24時間" in keyword or "急" in keyword:
            return "緊急対応"
        else:
            return "サービス検索"
    
    def calculate_opportunity_score(self, opportunity):
        """機会スコアを計算（簡易版）"""
        intent_scores = {"価格情報": 5, "緊急対応": 4, "サービス検索": 3, "評価・比較": 2, "情報収集": 1}
        strength_scores = {"弱": 3, "中": 2, "強": 1}
        
        intent_score = intent_scores.get(opportunity["検索意図"], 1)
        strength_score = strength_scores.get(opportunity["競合強度"], 1)
        
        return intent_score + strength_score
    
    def analyze_content_gaps(self, detailed_data):
        """コンテンツギャップを分析"""
        gaps = {
            "和光葬儀社が優位に立てる領域": [],
            "即座に対応すべき検索意図": []
        }
        
        # 和光葬儀社が圏外で、競合が弱い領域を特定
        for keyword, data in detailed_data.items():
            if data["和光葬儀社の順位"] == "圏外":
                # 大手チェーンが少ない場合は機会
                if data["競合分類"]["大手チェーン"] <= 2:
                    gaps["和光葬儀社が優位に立てる領域"].append(f"{keyword}: 大手チェーン少数")
                
                # 地域密着が多い場合も機会
                if data["競合分類"]["地域密着"] >= 3:
                    gaps["即座に対応すべき検索意図"].append(f"{keyword}: 地域特化コンテンツ強化")
        
        return gaps
    
    def extract_domain(self, url):
        """URLからドメイン名を抽出"""
        try:
            return urlparse(url).netloc
        except:
            return None
    
    def print_detailed_keyword_results(self, keyword, analysis):
        """詳細なキーワード分析結果をコンソールに表示"""
        print(f"  📊 {keyword}の詳細分析結果:")
        print(f"    🏆 和光葬儀社順位: {analysis['和光葬儀社の順位']}")
        print(f"    🌐 競合サイト数: {analysis['競合サイト数']}件")
        print(f"    📢 広告: {analysis['広告出稿状況']}")
        
        # 競合分類表示
        comp_class = analysis['競合分類']
        print(f"    🏢 競合内訳: 大手{comp_class['大手チェーン']}・地域{comp_class['地域密着']}・ポータル{comp_class['比較ポータル']}・情報{comp_class['情報サイト']}・他{comp_class['その他']}")
        
        # SERP機能
        serp_feat = analysis['SERP機能']
        features = []
        if serp_feat['local_pack']:
            features.append("ローカルパック")
        if serp_feat['ads_count'] > 0:
            features.append(f"広告{serp_feat['ads_count']}件")
        if serp_feat['paa_questions']:
            features.append("PAA")
        if serp_feat['knowledge_graph']:
            features.append("ナレッジ")
        
        print(f"    🎯 SERP機能: {', '.join(features) if features else 'なし'}")
        
        # 上位3サイト
        if analysis['上位競合サイト']:
            print(f"    🥇 TOP3: ", end="")
            top3 = [f"{i+1}位:{site['ドメイン']}" for i, site in enumerate(analysis['上位競合サイト'][:3])]
            print(" | ".join(top3))
        
        # 関連検索（最初の3つ）
        if analysis['関連検索']:
            related = analysis['関連検索'][:3]
            print(f"    🔗 関連: {', '.join(related)}")
    
    def save_comprehensive_results(self, results):
        """包括的な分析結果を保存"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # JSON形式で詳細データ保存
        try:
            os.makedirs("../outputs", exist_ok=True)
            filename = f"../outputs/seo-analysis-dynamic_{timestamp}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"\n💾 詳細分析結果を保存: {filename}")
        except Exception as e:
            print(f"⚠️ ファイル保存エラー: {e}")
        
        # Markdown形式でサマリー保存
        try:
            md_filename = f"../outputs/seo-analysis-summary_{timestamp}.md"
            self.generate_markdown_report(results, md_filename)
            print(f"📄 サマリーレポート保存: {md_filename}")
        except Exception as e:
            print(f"⚠️ Markdownレポート保存エラー: {e}")
    
    def generate_markdown_report(self, results, filename):
        """Markdownレポートを生成"""
        info = results["分析実行情報"]
        rank_info = results["リアルタイム順位・競合分析"]
        opportunities = results["動的発見キーワード機会"]
        
        md_content = f"""# 和光葬儀社 SEO分析・改善提案（SerpAPI動的分析結果）

## 分析実行情報
- **分析日時**: {info["分析日時"]}
- **使用API**: {info["使用API"]}
- **分析キーワード数**: {info["分析キーワード数"]}キーワード
- **データ取得成功率**: {info["データ取得成功率"]}

## リアルタイム順位・競合分析

### 現在の和光葬儀社順位状況
| キーワード | 現在順位 | 1位サイト | 2位サイト | 3位サイト |
|------------|----------|-----------|-----------|-----------|
"""
        
        # 順位状況テーブル生成
        for keyword, rank_data in rank_info["和光葬儀社順位状況"].items():
            rank = rank_data["順位"]
            top3 = rank_data["上位3サイト"]
            
            site1 = top3[0]["ドメイン"] if len(top3) > 0 else "-"
            site2 = top3[1]["ドメイン"] if len(top3) > 1 else "-"
            site3 = top3[2]["ドメイン"] if len(top3) > 2 else "-"
            
            md_content += f"| {keyword} | {rank} | {site1} | {site2} | {site3} |\n"
        
        # 競合分析結果
        comp_patterns = rank_info["競合SERP分析結果"]["主要競合パターン"]
        md_content += f"""
### 競合SERP分析結果

#### 主要競合パターン
"""
        
        for i, (domain, data) in enumerate(comp_patterns.items(), 1):
            md_content += f"""
{i}. **{domain}**: {data["出現キーワード数"]}キーワードで上位表示（平均{data["平均順位"]}位）
   - カテゴリ: {data["カテゴリ"]}
   - SEO戦略: {data["SEO戦略"]}
"""
        
        # SERP機能分析
        serp_features = rank_info["競合SERP分析結果"]["SERP機能分析"]
        md_content += f"""
#### SERP機能分析
- **ローカルパック表示**: {serp_features.get("ローカルパック表示", "データなし")}
- **広告表示**: {serp_features.get("広告表示", "データなし")}
- **PAA表示**: {serp_features.get("PAA表示", "データなし")}
- **ナレッジグラフ**: {serp_features.get("ナレッジグラフ", "データなし")}
"""
        
        # 新規キーワード機会
        new_keywords = opportunities["新規ターゲットキーワード"]
        md_content += f"""
## 動的発見キーワード機会

### 新規ターゲットキーワード（関連検索から発見）
"""
        
        for i, kw_data in enumerate(new_keywords, 1):
            md_content += f"{i}. **{kw_data['キーワード']}** - 検索意図: {kw_data['検索意図']} - 競合強度: {kw_data['競合強度']}\n"
        
        # コンテンツギャップ
        gaps = opportunities["コンテンツギャップ分析結果"]
        md_content += f"""
### コンテンツギャップ分析結果

#### 和光葬儀社が優位に立てる領域
"""
        for gap in gaps["和光葬儀社が優位に立てる領域"]:
            md_content += f"- {gap}\n"
        
        md_content += f"""
#### 即座に対応すべき検索意図
"""
        for intent in gaps["即座に対応すべき検索意図"]:
            md_content += f"1. {intent}\n"
        
        md_content += f"""
---
*このファイルはSerpAPIリアルタイムデータ（{info["分析日時"]}）に基づく分析結果です*
"""
        
        # ファイル保存
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(md_content)
    
    def print_comprehensive_summary(self, results):
        """包括的なサマリーを表示"""
        print("\n" + "=" * 70)
        print("📈 和光葬儀社 SEO動的分析 完了サマリー")
        print("=" * 70)
        
        info = results["分析実行情報"]
        print(f"📅 分析完了: {info['分析日時']}")
        print(f"🎯 分析成功率: {info['データ取得成功率']}")
        
        # 順位状況サマリー
        rank_info = results["リアルタイム順位・競合分析"]["和光葬儀社順位状況"]
        ranked_count = sum(1 for data in rank_info.values() if data["順位"] != "圏外")
        print(f"🏆 ランクイン: {ranked_count}/{len(rank_info)}キーワード")
        
        # 新規機会
        new_kw_count = len(results["動的発見キーワード機会"]["新規ターゲットキーワード"])
        print(f"🔍 新規機会: {new_kw_count}キーワード発見")
        
        # 競合状況
        comp_patterns = results["リアルタイム順位・競合分析"]["競合SERP分析結果"]["主要競合パターン"]
        top_competitor = list(comp_patterns.keys())[0] if comp_patterns else "不明"
        print(f"🏢 主要競合: {top_competitor}")
        
        print("=" * 70)
        print("📋 次のステップ:")
        print("  1. 生成されたMarkdownレポートでの詳細確認")
        print("  2. 新規キーワードの優先順位付け")
        print("  3. 競合ギャップを突くコンテンツ企画")
        print("  4. 定期実行（月1回）での順位変動監視")
        print("=" * 70)

def main():
    """メイン実行関数"""
    print("🚀 和光葬儀社 SEOキーワード動的分析ツール")
    print("📡 SerpAPI使用 - リアルタイム競合分析・キーワード機会発見")
    print("")
    
    # APIキー確認
    api_key = os.getenv("SERPAPI_KEY")
    if not api_key:
        print("❌ エラー: .envファイルのSERPAPI_KEYが設定されていません")
        print("📝 setup手順:")
        print("  1. env-template.txt を .env にコピー")
        print("  2. SerpAPIでアカウント作成・APIキー取得")
        print("  3. .envファイルにAPIキーを設定")
        print("  4. python test-serpapi.py で接続テスト")
        return
    
    # 分析実行
    analyzer = FuneralSEOAnalyzer(api_key)
    
    try:
        print("⏳ 動的SEO分析を開始...")
        results = analyzer.analyze_funeral_keywords_dynamic()
        
        print("\n✅ 分析完了！")
        print(f"📊 結果ファイル: outputs/フォルダを確認")
        print(f"🔄 定期実行推奨: 月1回の競合監視")
        
    except KeyboardInterrupt:
        print("\n⏹️ 分析を中断しました")
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")
        print("🔧 対処方法:")
        print("  1. インターネット接続を確認")
        print("  2. SerpAPIキーの有効性を確認")
        print("  3. API制限回数を確認")
    
    print("\n" + "=" * 50)
    input("Enterキーで終了...")

if __name__ == "__main__":
    main() 