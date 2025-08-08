# TARGET_COMPANY SEO分析・改善レポート（定量テンプレート）

## 実行日時
<!-- TODO_EXECUTION_DATE -->
<!-- /TODO_EXECUTION_DATE -->

## 使用データ
- @prompts/seo-analysis.md
- @output/YYYYMMDD/knowledge/company-info.md
- GA4 / GSC / PageSpeed Insights / Lighthouse など
- @output/01_competitor-analysis.md（競合10社・評価軸・スコアボード）

---

## エグゼクティブサマリー（数値要約）
<!-- TODO_EXEC_SUMMARY -->
- 現状スコアの総括（例: SEO健全性XX/100、主要KPIの推移）
- クリティカル課題（Top3）
- 想定インパクト（3ヶ月/6ヶ月の見込み指標）
<!-- /TODO_EXEC_SUMMARY -->

## 現状スコアボード
<!-- TODO_SCOREBOARD -->
- Lighthouse: Performance __ / Accessibility __ / Best Practices __ / SEO __
- Core Web Vitals: LCP __ ms / INP __ ms / CLS __
- PageSpeed Insights: Mobile __ / Desktop __
- インデックス: 有効 __ 件 / エラー __ 件 / 除外 __ 件
- 自然検索トラフィック（月次）: セッション __ / クリック __ / インプレッション __ / CTR __% / 平均掲載順位 __
- バックリンク: 合計 __ / 参照ドメイン __ / 権威指標（DA/DR 等） __
- インデックス済みページ数: __ / サイトマップ送信: はい/いいえ / robots: 問題なし/要確認
<!-- /TODO_SCOREBOARD -->

## キーワード分布（ブランド/非ブランド）
<!-- TODO_KEYWORD_DISTRIBUTION -->
| 種別 | Top3 | Top10 | Top20 | Top100 | 合計 |
|---|---:|---:|---:|---:|---:|
| ブランド |  |  |  |  |  |
| 非ブランド |  |  |  |  |  |
<!-- /TODO_KEYWORD_DISTRIBUTION -->

## 主要LP/ページ別検索実績（上位10件）
<!-- TODO_TOP_PAGES -->
| URL/タイトル | クリック | インプレッション | CTR | 平均掲載順位 | 直帰率 | CVR |
|---|---:|---:|---:|---:|---:|---:|
|  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |
<!-- /TODO_TOP_PAGES -->

## 技術ヘルスチェック（件数）
<!-- TODO_TECH_HEALTH -->
- 404/5xx: __ / __
- リダイレクトチェーン/ループ: __ / __
- 重複タイトル/メタ説明: __ / __
- H1欠如/重複: __ / __
- 大容量画像（>300KB）/未圧縮画像: __ / __
- 未使用JS/レンダーブロック資産（合計KB）: __ / __
- CLS高リスクページ数（>0.25）: __
- モバイルユーザビリティ問題ページ数: __
- 構造化データ エラー/警告: __ / __
<!-- /TODO_TECH_HEALTH -->

## 競合ベンチマーク（01の10社から選定、3-5社）
<!-- TODO_COMPETITOR_MAPPING -->
参照元: @output/01_competitor-analysis.md の企業番号 → 本表の企業名
- 例）#1 企業A → 競合A、#3 企業C → 競合B、#5 企業E → 競合C
<!-- /TODO_COMPETITOR_MAPPING -->
<!-- TODO_COMPETITOR_BENCH -->
| 指標 | 自社 | 競合A | 競合B | 競合C |
|---|---:|---:|---:|---:|
| 自然クリック（月） |  |  |  |  |
| 平均掲載順位 |  |  |  |  |
| Top10キーワード数 |  |  |  |  |
| バックリンク/参照ドメイン |  /  |  /  |  /  |  /  |
| LCP(ms)/INP(ms)/CLS |  /  /  |  /  /  |  /  /  |  /  /  |
<!-- /TODO_COMPETITOR_BENCH -->

## キーワードクラスター（Head/Middle/Long-tail）
<!-- TODO_KEYWORD_CLUSTERS -->
| クラスター | 検索意図 | ボリューム | 難易度(KD) | 現在順位 | 目標順位 | 期待クリック増 | 優先度 |
|---|---|---:|---:|---:|---:|---:|---|
| Head |  |  |  |  |  |  |  |
| Middle |  |  |  |  |  |  |  |
| Long-tail |  |  |  |  |  |  |  |
<!-- /TODO_KEYWORD_CLUSTERS -->

## ロングテール・ニッチ分析（地域×サービスなど）
<!-- TODO_LONGTAIL_NICHE -->
| テーマ/組み合わせ | 代表KW | SV | KD | 意図 | SERP特徴 | 既存/新規 | 推定クリック | 推奨ページ |
|---|---|---:|---:|---|---|---|---:|---|
| 地域A × サービスX |  |  |  |  |  | 既存/新規 |  |  |
| 地域B × サービスY |  |  |  |  |  | 既存/新規 |  |  |
| ニッチ課題Z |  |  |  |  |  | 既存/新規 |  |  |
<!-- /TODO_LONGTAIL_NICHE -->

## コンテンツギャップ（要約）
<!-- TODO_CONTENT_GAP -->
- 未カバーの検索意図/テーマ数: __
- 作成推奨ページ案: __ 件（例: 比較/料金/事例/地域特化 等）
<!-- /TODO_CONTENT_GAP -->

## 優先施策バックログ（期待効果・工数付き）
<!-- TODO_ACTION_BACKLOG -->
| 優先度 | 施策 | 影響指標 | 現状 | 目標 | 期待効果(クリック/セッション%) | 工数(人日) | 期間 |
|---|---|---|---:|---:|---:|---:|---|
| P1 |  |  |  |  |  |  |  |
| P1 |  |  |  |  |  |  |  |
| P2 |  |  |  |  |  |  |  |
| P3 |  |  |  |  |  |  |  |
<!-- /TODO_ACTION_BACKLOG -->

## KPIとターゲット
<!-- TODO_KPI_TARGETS -->
| KPI | ベースライン | 3ヶ月 | 6ヶ月 | 12ヶ月 | 計測元 |
|---|---:|---:|---:|---:|---|
| 自然クリック（月） |  |  |  |  | GSC |
| CTR |  |  |  |  | GSC |
| 平均掲載順位 |  |  |  |  | GSC |
| セッション（月） |  |  |  |  | GA4 |
| CVR |  |  |  |  | GA4 |
| LCP/INP/CLS |  /  /  |  /  /  |  /  /  |  /  /  | PSI/LH |
<!-- /TODO_KPI_TARGETS -->

## 効果予測（算定根拠）
<!-- TODO_IMPACT_MODEL -->
- 前提: ランク上昇Δrに対するCTR曲線を用い、クリック増分=インプレッション×(CTR_new−CTR_base)
- 施策別想定: 例）コンテンツ追加 n本 → Top10キーワード +m、クリック +x%
- リスク・感度: 悲観/中央値/楽観の3ケース
<!-- /TODO_IMPACT_MODEL -->

## 計測・モニタリング設計
<!-- TODO_MEASUREMENT_PLAN -->
- ダッシュボード: 週次（GA4/GSC/PSI/LH）
- アラート: CWV閾値超過、404急増、クリック急減
- ログ: 変更履歴（タイトル/H1/内部リンク/サイトマップ提出 等）
<!-- /TODO_MEASUREMENT_PLAN -->

---
*このファイルはAIが生成した結果です*