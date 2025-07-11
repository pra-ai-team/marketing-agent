# 和光葬儀社 ランディングページ

## 📋 プロジェクト概要

和光葬儀社の新規ランディングページ制作プロジェクトです。マーケティング戦略に基づき、コンバージョン率3.5%以上を目標とした高性能LPを制作しました。

### 🎯 主要目標
- **電話問い合わせ数**: 月間150件→225件（50%増）
- **コンバージョン率**: 3.5%以上（業界平均2.1%を大幅超越）
- **ターゲット**: 急需要層（50-70代）+ 事前相談層（60-80代）

## 🗂️ ファイル構成

```
lp-files/
├── index.html          # メインHTMLファイル
├── style.css           # CSSスタイルシート
├── script.js           # JavaScript機能
└── README.md           # このファイル
```

## 🏗️ ページ構成

### 1. ファーストビュー
- **目的**: 3秒以内で信頼感と安心感を提供
- **要素**: 価格明示、24時間対応、口コミNo.1、電話番号大型表示
- **CTA**: 「今すぐ相談する」「事前相談申込み」

### 2. 選ばれる理由（4つの差別化要素）
- 価格透明性（追加料金なし162,800円）
- 24時間365日対応
- Google口コミ件数神奈川県No.1
- 有資格者在籍（1・2級葬祭ディレクター）

### 3. サービス・料金
- 直葬プラン詳細（162,800円）
- その他プラン（家族葬・一般葬）
- 追加料金なし保証

### 4. お客様の声・実績
- 統計数値（年間対応件数、満足度、評価）
- Google口コミ抜粋（3件）

### 5. 安心のサポート体制
- 有資格者在籍、24時間対応
- アフターサポート、各種決済対応

### 6. よくある質問
- 重要FAQ 5項目
- アコーディオン形式で表示

### 7. お問い合わせ
- 電話とフォームの2つの導線
- 営業情報の明記

## 🎨 デザイン仕様

### カラーパレット
- **プライマリ**: 深紺（#1e3a8a） - 信頼感・安心感
- **セカンダリ**: 金色（#d4af37） - 格式・品格
- **アクセント**: 緊急赤（#dc2626） - CTAボタン
- **テキスト**: ダークグレー（#374151）

### タイポグラフィ
- **見出し**: 明朝体（Noto Serif JP）
- **本文**: ゴシック体（Noto Sans JP）
- **電話番号**: 太字・大サイズ（32px以上）

### レスポンシブ対応
- モバイルファースト設計
- ブレークポイント: 768px, 480px
- 高齢者配慮の視認性最適化

## 🚀 技術仕様

### HTML
- セマンティックHTML5
- 構造化データ実装（LocalBusiness, FAQPage）
- SEO最適化（メタタグ、OGP）
- アクセシビリティ対応

### CSS
- CSS Grid / Flexbox レイアウト
- CSS変数（カスタムプロパティ）活用
- アニメーション・トランジション
- モバイル最適化

### JavaScript
- FAQアコーディオン機能
- スムーススクロール
- フォーム送信処理
- イベント計測（Google Analytics）
- パフォーマンス監視

## 📊 計測・分析機能

### Google Analytics イベント
- 電話クリック追跡
- フォーム送信追跡
- CTAボタンクリック追跡
- スクロール深度追跡
- セクション表示追跡

### 主要KPI
- **コンバージョン率**: 3.5%以上
- **電話発信率**: 5.0%以上
- **滞在時間**: 2分以上
- **直帰率**: 65%以下

## ⚡ パフォーマンス最適化

### 表示速度対策
- 画像最適化（WebP形式推奨）
- CSS/JavaScript圧縮
- 重要リソースの先読み（preload/prefetch）
- レイジーローディング実装

### Core Web Vitals
- **LCP**: 2.5秒以内
- **FID**: 100ms以内
- **CLS**: 0.1以下

## 🔧 セットアップ手順

### 1. ファイル配置
```bash
# Webサーバーのドキュメントルートに配置
├── index.html
├── style.css
├── script.js
└── images/（画像ファイル）
```

### 2. Google Analytics 設定
```html
<!-- index.html の head タグ内に追加 -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

### 3. フォーム送信先設定
```javascript
// script.js の submitForm 関数内で設定
fetch('/api/contact', {
    method: 'POST',
    body: formData
})
```

### 4. 電話番号設定確認
- すべての `tel:0120-05-2194` が正しく設定されているか確認
- 必要に応じて番号を変更

## 🧪 テスト項目

### 機能テスト
- [ ] 電話リンクの動作確認
- [ ] フォーム送信処理
- [ ] FAQアコーディオンの動作
- [ ] スムーススクロール
- [ ] レスポンシブ表示

### パフォーマンステスト
- [ ] PageSpeed Insights で90点以上
- [ ] モバイル表示速度3秒以内
- [ ] 各デバイスでの表示確認

### アクセシビリティテスト
- [ ] キーボードナビゲーション
- [ ] スクリーンリーダー対応
- [ ] カラーコントラスト比4.5:1以上

## 📈 A/Bテスト項目

### 優先実施項目
1. **ファーストビューのキャッチコピー**
   - 現行: 「追加料金一切なし162,800円｜横浜の葬儀なら24時間対応」
   - 候補: 「神奈川県口コミNo.1｜追加料金なし162,800円の安心葬儀」

2. **CTAボタンの文言**
   - 現行: 「今すぐ相談する」
   - 候補: 「24時間無料相談」「今すぐ電話する」

3. **お客様の声の配置**
   - 現行: 実績セクション内
   - 候補: ファーストビュー直下

### 測定方法
- Google Optimize または類似ツール使用
- 統計的有意性確保（最低2週間、サンプル数1000以上）
- 主要KPI（CV率、電話発信率）で評価

## 🛠️ 改善提案

### 短期改善（1ヶ月以内）
1. **画像の追加・最適化**
   - 実際の葬儀会場写真
   - スタッフ写真（信頼性向上）
   - WebP形式での配信

2. **マイクロコピーの最適化**
   - フォーム項目の説明文追加
   - エラーメッセージの改善
   - 送信後メッセージの詳細化

3. **口コミ表示の強化**
   - Google口コミのスクリーンショット
   - 星評価の視覚的強化
   - 口コミ件数の具体的数値表示

### 中期改善（3ヶ月以内）
1. **コンテンツ追加**
   - 葬儀の流れ詳細ページ
   - 費用シミュレーター
   - 事前相談予約カレンダー

2. **インタラクティブ要素**
   - チャットボット導入
   - 価格計算ツール
   - 資料ダウンロード機能

3. **パーソナライゼーション**
   - 地域別コンテンツ表示
   - リターゲティング広告連携
   - 行動データに基づく最適化

### 長期改善（6ヶ月以内）
1. **PWA化**
   - オフライン対応
   - プッシュ通知機能
   - ホーム画面追加促進

2. **AI活用**
   - チャットボットの高度化
   - 自動見積もりシステム
   - 予測分析による最適化

3. **マルチデバイス対応強化**
   - タブレット専用レイアウト
   - 音声検索対応
   - スマートスピーカー連携

## 🎯 成功指標

### 短期目標（3ヶ月）
- コンバージョン率: 3.5%達成
- 電話問い合わせ: 月間200件
- ページ表示速度: モバイル3秒以内

### 中期目標（6ヶ月）
- コンバージョン率: 4.0%
- 月間問い合わせ: 225件
- Google口コミ: 月間新規20件

### 長期目標（12ヶ月）
- 神奈川県内検索順位: 「葬儀 横浜」1位
- 市場シェア: 県内Top3入り
- ブランド認知度: 70%以上

## 📞 サポート・連絡先

### 技術サポート
- HTML/CSS/JavaScript の修正・カスタマイズ
- Google Analytics 設定サポート
- パフォーマンス最適化

### マーケティングサポート
- A/Bテスト実施支援
- コンバージョン率改善提案
- SEO対策アドバイス

---

**制作日**: 2025年1月16日  
**制作者**: AI Marketing Agent  
**バージョン**: 1.0  
**最終更新**: 2025年1月16日 