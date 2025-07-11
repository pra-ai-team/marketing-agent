#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
汎用マーケティングツール設定ファイルローダー

project-config.yamlから設定を読み込み、プロジェクトに応じた
動的な企業・業界情報を提供する

使用方法:
    from workflows.config_loader import ConfigLoader
    config = ConfigLoader()
    company_info = config.get_company_info()
    industry_info = config.get_industry_info()
"""

import yaml
import os
import sys
from pathlib import Path
from datetime import datetime

class ConfigLoader:
    def __init__(self, config_path=None):
        """
        設定ファイルローダーの初期化
        
        Args:
            config_path: 設定ファイルのパス（デフォルト: config/project-config.yaml）
        """
        if config_path is None:
            config_path = "config/project-config.yaml"
        
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self):
        """設定ファイルを読み込む"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"❌ 設定ファイルが見つかりません: {self.config_path}")
            print("📋 設定ファイルの作成方法:")
            print("1. config/project-config.yaml を作成してください")
            print("2. 企業・業界情報を記入してください")
            print("3. 再度実行してください")
            sys.exit(1)
        except yaml.YAMLError as e:
            print(f"❌ 設定ファイルの読み込みに失敗しました: {e}")
            sys.exit(1)
    
    def get_company_info(self):
        """企業情報を取得"""
        return self.config.get('company', {})
    
    def get_industry_info(self):
        """業界情報を取得"""
        return self.config.get('industry', {})
    
    def get_competitors_info(self):
        """競合情報を取得"""
        return self.config.get('competitors', {})
    
    def get_seo_config(self):
        """SEO設定を取得"""
        return self.config.get('seo', {})
    
    def get_target_customers(self):
        """ターゲット顧客情報を取得"""
        return self.config.get('target_customers', {})
    
    def get_marketing_goals(self):
        """マーケティング目標を取得"""
        return self.config.get('marketing_goals', {})
    
    def get_landing_page_config(self):
        """LP設定を取得"""
        return self.config.get('landing_page', {})
    
    def get_quality_control_config(self):
        """品質管理設定を取得"""
        return self.config.get('quality_control', {})
    
    def validate_config(self):
        """設定内容の妥当性をチェック"""
        errors = []
        warnings = []
        
        # 必須フィールドのチェック
        company = self.get_company_info()
        if not company.get('name') or 'を入力してください' in company.get('name', ''):
            errors.append("企業名が設定されていません")
        
        if not company.get('industry') or 'を入力してください' in company.get('industry', ''):
            errors.append("業界が設定されていません")
        
        if not company.get('location') or 'を入力してください' in company.get('location', ''):
            errors.append("営業地域が設定されていません")
        
        # 競合情報のチェック
        competitors = self.get_competitors_info()
        target_companies = competitors.get('target_companies', [])
        if not target_companies or len(target_companies) < 3:
            warnings.append("競合企業は3社以上設定することを推奨します")
        
        # SEO設定のチェック
        seo = self.get_seo_config()
        if not seo.get('primary_keywords') or len(seo.get('primary_keywords', [])) < 3:
            warnings.append("メインキーワードは3個以上設定することを推奨します")
        
        return errors, warnings
    
    def generate_knowledge_base(self):
        """設定情報から知識ベースを生成"""
        company = self.get_company_info()
        industry = self.get_industry_info()
        competitors = self.get_competitors_info()
        seo = self.get_seo_config()
        
        knowledge_base = f"""# {company.get('name', 'TARGET_COMPANY')} - 企業・業界情報

## 企業概要

### 基本情報
- **企業名**: {company.get('name', 'TARGET_COMPANY')}
- **サービス名**: {company.get('business_name', 'TARGET_SERVICE')}
- **業界**: {company.get('industry', 'TARGET_INDUSTRY')}
- **主要営業地域**: {company.get('location', 'TARGET_LOCATION')}
- **都道府県**: {company.get('prefecture', 'TARGET_PREFECTURE')}
- **市区町村**: {company.get('city', 'TARGET_CITY')}

### 企業の特徴・強み
"""
        
        # 特徴・強みを追加
        for feature in company.get('key_features', []):
            knowledge_base += f"- {feature}\n"
        
        knowledge_base += f"""
### サービス・料金
- **主要サービス**: {company.get('services', {}).get('primary_service', 'PRIMARY_SERVICE')}
- **価格帯**: {company.get('services', {}).get('price_range', 'PRICE_RANGE')}
- **特別プラン**: {company.get('services', {}).get('special_offers', 'SPECIAL_OFFERS')}

### 連絡先・営業情報
- **電話**: {company.get('contact', {}).get('phone', 'PHONE_NUMBER')}
- **メール**: {company.get('contact', {}).get('email', 'EMAIL_ADDRESS')}
- **ウェブサイト**: {company.get('contact', {}).get('website', 'WEBSITE_URL')}
- **営業時間**: {company.get('contact', {}).get('hours', 'BUSINESS_HOURS')}

## 業界情報

### 業界概要
- **業界名**: {industry.get('name', 'TARGET_INDUSTRY')}
- **市場規模**: {industry.get('market_size', 'MARKET_SIZE')}
- **成長率**: {industry.get('growth_rate', 'GROWTH_RATE')}

### 業界の特徴
"""
        
        # 業界特徴を追加
        for characteristic in industry.get('characteristics', []):
            knowledge_base += f"- {characteristic}\n"
        
        knowledge_base += "\n### 顧客特性\n"
        for behavior in industry.get('customer_behavior', []):
            knowledge_base += f"- {behavior}\n"
        
        knowledge_base += "\n### 主要な課題\n"
        for challenge in industry.get('challenges', []):
            knowledge_base += f"- {challenge}\n"
        
        knowledge_base += "\n## 競合分析対象\n\n"
        
        # 競合企業リストを追加
        for i, competitor in enumerate(competitors.get('target_companies', []), 1):
            knowledge_base += f"### 競合{i}: {competitor.get('name', 'COMPETITOR_NAME')}\n"
            knowledge_base += f"- **ウェブサイト**: {competitor.get('website', 'WEBSITE_URL')}\n"
            knowledge_base += f"- **カテゴリ**: {competitor.get('category', 'CATEGORY')}\n\n"
        
        knowledge_base += "\n## SEO・マーケティング情報\n\n"
        knowledge_base += "### ターゲットキーワード\n\n"
        knowledge_base += "**メインキーワード**:\n"
        for keyword in seo.get('primary_keywords', []):
            knowledge_base += f"- {keyword}\n"
        
        knowledge_base += "\n**サブキーワード**:\n"
        for keyword in seo.get('secondary_keywords', []):
            knowledge_base += f"- {keyword}\n"
        
        knowledge_base += "\n**地域特化キーワード**:\n"
        for keyword in seo.get('local_keywords', []):
            knowledge_base += f"- {keyword}\n"
        
        return knowledge_base
    
    def generate_project_summary(self):
        """プロジェクトサマリーを生成"""
        company = self.get_company_info()
        industry = self.get_industry_info()
        goals = self.get_marketing_goals()
        
        return f"""# プロジェクトサマリー

## 対象企業
- **企業名**: {company.get('name', 'TARGET_COMPANY')}
- **業界**: {company.get('industry', 'TARGET_INDUSTRY')}
- **地域**: {company.get('location', 'TARGET_LOCATION')}

## プロジェクト目標
- **主要目標**: {goals.get('primary_goal', 'PRIMARY_GOAL')}
- **達成期間**: {goals.get('timeline', 'TIMELINE')}
- **予算**: {goals.get('budget', 'BUDGET')}

## 期待される成果
"""
        
        for metric in goals.get('target_metrics', []):
            return f"- {metric}\n"
    
    def print_config_summary(self):
        """設定内容のサマリーを表示"""
        print("📋 プロジェクト設定サマリー")
        print("=" * 50)
        
        company = self.get_company_info()
        print(f"企業名: {company.get('name', '未設定')}")
        print(f"業界: {company.get('industry', '未設定')}")
        print(f"地域: {company.get('location', '未設定')}")
        
        competitors = self.get_competitors_info()
        print(f"競合企業数: {len(competitors.get('target_companies', []))}社")
        
        seo = self.get_seo_config()
        print(f"メインキーワード数: {len(seo.get('primary_keywords', []))}個")
        
        print("=" * 50)
        
        # 設定の妥当性チェック
        errors, warnings = self.validate_config()
        
        if errors:
            print("❌ 設定エラー:")
            for error in errors:
                print(f"  - {error}")
        
        if warnings:
            print("⚠️ 設定警告:")
            for warning in warnings:
                print(f"  - {warning}")
        
        if not errors and not warnings:
            print("✅ 設定は正常です")

def main():
    """設定ファイルの内容を確認"""
    config = ConfigLoader()
    config.print_config_summary()
    
    # 知識ベースの生成テスト
    print("\n📚 知識ベース生成テスト")
    print("=" * 50)
    knowledge_base = config.generate_knowledge_base()
    print(knowledge_base[:500] + "..." if len(knowledge_base) > 500 else knowledge_base)

if __name__ == "__main__":
    main() 