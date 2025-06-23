# 🚀 マーケティング企画・制作エージェント

> **和光葬儀社向け**　AI駆動型マーケティング戦略立案・LP制作システム

## 📋 概要

葬儀業界に特化したマーケティング戦略の立案からランディングページ制作まで、一連のプロセスを自動化・効率化するCursor専用システムです。

### 🎯 対象企業
- **企業名**: 株式会社和光商事：和光葬儀社
- **業界**: 葬儀サービス業  
- **地域**: 横浜市（神奈川県）
- **特徴**: 24時間365日対応、明朗価格、Google口コミ件数神奈川県No.1

### ⚡ 5分でスタート

```bash
# 1. プロジェクト作成
python workflows/setup-project.py

# 2. Cursorでプロンプト実行
# @prompts/quick-start.md の内容をコピーして実行
```

### 🎯 最終成果物

- ✅ **競合分析レポート** - 葬儀業界の詳細な競合状況分析
- ✅ **SEO最適化戦略** - キーワード選定・検索エンジン対策
- ✅ **マーケティング戦略** - 包括的な戦略・ペルソナ・KPI設定  
- ✅ **LP要件定義書** - 実装可能な詳細仕様
- ✅ **高品質LP** - 即座に公開可能なHTML/CSS/JS

## 📁 プロジェクト構成

```
マーケティング企画・制作エージェント/
├── 📋 prompts/              # プロンプトテンプレート
│   ├── quick-start.md       # ⭐ クイックスタートプロンプト
│   ├── competitor-analysis.md
│   ├── seo-analysis.md
│   └── lp-development.md
├── 📚 knowledge/            # ナレッジベース
│   ├── wakousougisya-company-info.md  # 企業情報
│   ├── funeral-industry.md            # 業界情報
│   └── funeral-seo-keywords.md        # SEOキーワード
├── ⚙️ workflows/            # 自動化ツール
│   ├── main.md              # ⭐ メインワークフロー定義
│   ├── setup-project.py     # プロジェクト自動セットアップ
│   ├── check-progress.py    # 進捗確認ツール  
│   └── seo-keyword-analyzer.py  # SEO分析ツール
└── 📂 outputs/              # 成果物格納
    ├── templates/           # テンプレートファイル
    └── YYYYMMDD/           # 日付別プロジェクト
```

## 🚀 使用方法

### 方法1: クイックスタート（推奨）
```bash
# プロジェクト作成
python workflows/setup-project.py

# Cursorで以下をコピペして実行
@prompts/quick-start.md
```

### 方法2: 段階的実行
```bash
# 1. プロジェクト準備
python workflows/setup-project.py --date 20250625

# 2. 各STEPを順次実行
# @workflows/main.md を参照しながら進める
```

### 方法3: 進捗確認付き
```bash
# 進捗をリアルタイム確認
python workflows/check-progress.py

# TODOマーカー残存確認
findstr /n "TODO" outputs\YYYYMMDD\*.md
```

## 🎛️ システムの特徴

### ✨ AI最適化設計
- **プロンプト最適化**: Cursor専用に設計されたプロンプトテンプレート
- **自動品質管理**: TODOマーカーシステムによる進捗管理
- **継続的改善**: 実プロジェクトのフィードバックを反映

### 🔧 自動化機能
- **プロジェクトセットアップ**: ワンコマンドで環境準備完了
- **進捗確認**: リアルタイムで完了率・残タスク確認
- **SEO分析**: SerpAPI連携による自動キーワード分析

### 📊 品質保証
- **段階的検証**: 各STEPで前の結果を必ず参照
- **完全性チェック**: TODOマーカー残存の自動確認
- **実用性重視**: 即座に使用可能な成果物品質

## ⚙️ 技術環境

### 必要ツール
```bash
# Python環境（推奨: 3.8+）
pip install -r workflows/requirements.txt

# SerpAPI設定（SEO分析用・オプション）
setx SERPAPI_KEY "your_api_key_here"
```

### 対応環境
- **OS**: Windows 10/11 (PowerShell)
- **エディタ**: Cursor（必須）
- **Python**: 3.8+ 
- **API**: SerpAPI（SEO分析用・オプション）

## 📊 成功指標

### プロジェクト完了の目安
- [ ] 全5つのSTEPファイルが作成済み
- [ ] TODOマーカーが0個（完全に更新済み）
- [ ] LPがブラウザで正常表示
- [ ] SEO最適化スコア80%以上

### 品質チェックリスト  
- [ ] 競合優位性が明確に表現されている
- [ ] ターゲットキーワードが適切に配置
- [ ] レスポンシブデザインが機能
- [ ] ページ表示速度が3秒以内

## 🆘 トラブルシューティング

### よくある問題

**❓ プロジェクトが作成されない**
```bash
# ディレクトリ権限を確認
mkdir outputs
python workflows/setup-project.py
```

**❓ TODOマーカーが残っている**
```bash
# 進捗確認
python workflows/check-progress.py

# 手動確認
findstr /n "TODO" outputs\20250625\*.md
```

**❓ SerpAPI エラー**
```bash
# API キー設定確認
echo $env:SERPAPI_KEY
setx SERPAPI_KEY "your_api_key_here"
```

## 🔄 バージョン情報

- **現在バージョン**: v2.0 (2025年6月25日)
- **対応業界**: 葬儀サービス業
- **対応企業**: 和光葬儀社

### 🔮 今後の予定
- [ ] 他業界テンプレートの追加
- [ ] LP制作の自動化強化  
- [ ] A/Bテスト機能の実装

---

## 🚀 今すぐ始める

```bash
# プロジェクト作成
python workflows/setup-project.py

# Cursorで実行
@prompts/quick-start.md
```

**🎯 目標**: 和光葬儀社が即座に使用可能な、高品質なマーケティング戦略とランディングページの提供

---
*最終更新: 2025年6月25日* 