# ユーザー入力シート（このファイルに直接記入してください）

このファイルは、ユーザーが記入 → AIが補完・整形 → `input/project-config.yaml` に反映するための入力フォームです。
各項目の「ここに入力」の行だけを書き換えてください。例は削除して構いません。

---

## 1. 最小入力（最優先で記入）
※ この2項目があれば開始できます。

### 1-1. 企業名【必須】
- ここに入力: 株式会社富士越
- 例: 株式会社サンプル
- 反映先: `company.name`

### 1-2. 主な営業地域【必須】
- ここに入力: （例: 東京都新宿区）
- 都道府県: 東京都
- 市区町村: 中野区
- 反映先: `company.location`, `company.prefecture`, `company.city`

### 1-3. 公式サイトURL【任意】
- ここに入力:https://fujikoshi.net/
- 反映先: 参照用（存在しない場合は空で可）

---

## 2. あると精度が上がる入力（任意）
入力がなくてもAIが検索・補完しますが、記入すると精度が向上します。

### 2-1. サービス/ブランド名
- ここに入力: 
- 反映先: `company.business_name`

### 2-2. 強み・特徴（箇条書きで3件以上推奨）
- ここに入力1: 
- ここに入力2: 
- ここに入力3: 
- 反映先: `company.key_features[]`

### 2-3. 競合候補（名前 / URL / カテゴリ）
- 競合1 名前: ここに入力
  - URL: ここに入力（例: https://example.com）
  - カテゴリ: ここに入力（例: 大手チェーン/地域密着/オンライン/その他）
- 競合2 名前: ここに入力
  - URL: ここに入力
  - カテゴリ: ここに入力
- 競合3 名前: ここに入力
  - URL: ここに入力
  - カテゴリ: ここに入力
- 反映先: `competitors.target_companies[]`

### 2-4. キャンペーン・特別オファー
- ここに入力: 
- 反映先: `company.services.special_offers`

### 2-5. 連絡先
- 電話: ここに入力
- メール: ここに入力
- 反映先: `company.contact.phone`, `company.contact.email`

### 2-6. LPの目的 / 想定アクション
- 目的: ここに入力（例: 問い合わせ獲得、資料請求）
- アクション: ここに入力（例: 電話、フォーム送信）
- 反映先: `landing_page.purpose`, `landing_page.target_action`

### 2-7. デザイン傾向
- ここに入力: （例: シンプル/高級感/親しみやすさ/ミニマル など）
- 反映先: `landing_page.design_preference`

### 2-8. 掲載NG・避けたい表現
- ここに入力: 
- 反映先: メモとして保持（品質チェック工程で参照）

### 2-9. ターゲット顧客メモ
- ここに入力: （例: 年齢層/状況/ニーズ/検索行動のヒント）
- 反映先: `target_customers` の初期ヒント

---

## 3. AIが自動で補完・生成する項目（記入不要）
- 業界の特定と要約（`company.industry`, `industry.*`）
- 想定競合の抽出（`competitors.target_companies` の初期候補）
- 初期SEOキーワード案の作成（`seo.*`）
- 知識ベース・サマリー生成（`output/knowledge/company-info.md`, `output/project-summary.md`）

---

## 4. 実行メモ（参考）
- クイック開始（会社名と地域だけ記入済みを想定）
  - 例: `python workflows/setup-project.py --quick --force`
- 設定反映で実行
  - 例: `python workflows/setup-project.py --force`

---
注意: 本ファイルはAIによって解析され、`input/project-config.yaml` に反映されます。実行スクリプトは本ファイル自体を直接参照しません。
