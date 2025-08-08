# メイン実行プロンプト（自動連鎖オーケストレーション）

目的: 本プロンプトを実行すると、設定同期→雛形生成→各 STEP の自動補完→進捗/品質チェックまでを、直前の STEP の成果を参照しながら自動で連鎖実行します。

前提条件
- OS: Windows 10/11
- Python 3.8+
- 実行ディレクトリ: `marketing-agent/`
- 依存関係は未導入でも可（本プロンプト内で導入）
- 入力フォーム: ルート直下の `user_input.md`（最低: 企業名・地域、可能なら競合 URL も）

実行前の準備（最短）
1. 企業名を `input/company-name.txt` に1行で記入（例: 株式会社サンプル）
2. 本プロンプトの手順に従って実行

実行前の準備（従来）
1. 設定確認
   ```bash
   python src/workflows/config_loader.py
   ```
2. 設定に問題がある場合は `input/project-config.yaml` を編集して再確認
3. プロジェクト作成
   ```bash
   python src/workflows/setup-project.py
   ```

全体フロー
1. 依存関係導入（非対話）
2. 設定同期: `user_input.md` → `input/project-config.yaml` 反映
3. セットアップ実行: `output/YYYYMMDD/` を作成し、雛形展開/簡易置換/知識生成/競合収集/要件注入
4. 対象プロジェクト日付を決定（最新の `output/YYYYMMDD/`）
5. STEP1-5 を順に自動補完（前 STEP の成果を参照して TODO マーカーを削減）
6. 進捗と品質チェック（完了率、必須観点の網羅）→ 不足があれば差分追記

実行手順（自動連鎖）

STEP 0. 依存関係の確認・差分導入（非対話）
```bash
python src/workflows/ensure_deps.py
```

STEP 1. 設定同期とセットアップ（`user_input.md` を `input/project-config.yaml` に反映し、雛形生成）
```bash
python src/workflows/setup-project.py --quick --force
```
補足:
- クイックモードでは不足設定を警告扱いとし、企業名のみでも開始できます。
- 競合 URL が `input/project-config.yaml > competitors.target_companies` に設定されていれば自動収集し、`competitors/` 配下に保存します。

終了時チェック（前 STEP: STEP 0）
- `src/workflows/ensure_deps.py` がエラーなく完了していること。
- 必要な依存関係が導入済みであること。

STEP 2. 対象プロジェクトの決定
- 最新の `output/YYYYMMDD/` を対象とする。
- 以降、このディレクトリを `PROJECT_DIR` と呼ぶ。

終了時チェック（前 STEP: STEP 1）
- `PROJECT_DIR` が最新の `output/YYYYMMDD/` を正しく指していること。
- `PROJECT_DIR` に初期雛形（`01_competitor-analysis.md`, `02_seo-analysis.md`, `03_marketing-strategy.md`, `04_lp-requirements.md`）が存在すること。
- （適用可能な場合）前 STEP の TODO マーカーが残っていないこと。

STEP 3. 競合分析（STEP1）の自動補完
- 参照元:
  - `PROJECT_DIR/competitors/summary.md`
  - `PROJECT_DIR/competitors/*/summary.md`
  - `PROJECT_DIR/knowledge/company-info.md`
- 実行内容:
  - `PROJECT_DIR/01_competitor-analysis.md` の `<!-- TODO_... -->` を可能な範囲で自動補完する。
  - 競合一覧・スコアボードは `competitors.target_companies` と取得サマリから初期値を自動充填。
  - 要約・推奨アクションは見出し構造/CTA/差別化要素から要点を抽出し、箇条書きで記述。

終了時チェック（前 STEP: STEP 2）
- `PROJECT_DIR` が存在し、読み書き可能であること。
- （適用可能な場合）前 STEP の TODO マーカーが残っていないこと。

STEP 4. SEO・キーワード分析（STEP2）の自動補完
- 参照元:
  - `PROJECT_DIR/01_competitor-analysis.md` の結果
  - `input/project-config.yaml > seo.*`
  - `PROJECT_DIR/knowledge/company-info.md`
- 実行内容:
  - `PROJECT_DIR/02_seo-analysis.md` の `<!-- TODO_... -->` を自動補完する。
  - 主要/サブ/ローカル/ロングテールの候補を設定と競合情報から抽出。
  - 技術改善/内部リンク/優先度/測定方法を明文化。

終了時チェック（前 STEP: STEP 3）
- `PROJECT_DIR/01_competitor-analysis.md` が存在すること。
- 同ファイルに TODO マーカーが残っていないこと（Windows 例）:
```bash
findstr /n "TODO" %PROJECT_DIR%\01_competitor-analysis.md
```

STEP 5. マーケティング戦略（STEP3）の自動補完
- 参照元: STEP1-2 の成果、`input/project-config.yaml > marketing_goals`, `target_customers`
- 実行内容: `PROJECT_DIR/03_marketing-strategy.md` を自動補完し、KPI・予算・体制・リスク管理まで具体化。

終了時チェック（前 STEP: STEP 4）
- `PROJECT_DIR/02_seo-analysis.md` が存在すること。
- 同ファイルに TODO マーカーが残っていないこと（Windows 例）:
```bash
findstr /n "TODO" %PROJECT_DIR%\02_seo-analysis.md
```

STEP 6. LP 要件定義（STEP4）の自動補完
- 参照元: 競合LP差し込み（`04_lp-requirements.md` への自動注入済み）、STEP1-3 の成果
- 実行内容: `PROJECT_DIR/04_lp-requirements.md` の `<!-- TODO_... -->` を自動補完する（FV/CTA/導線/必須/推奨機能/分析設計）。

終了時チェック（前 STEP: STEP 5）
- `PROJECT_DIR/03_marketing-strategy.md` が存在すること。
- 同ファイルに TODO マーカーが残っていないこと（Windows 例）:
```bash
findstr /n "TODO" %PROJECT_DIR%\03_marketing-strategy.md
```

STEP 7. LP 制作（STEP5、任意だが推奨）
- `PROJECT_DIR/lp-files/` が無い場合は作成し、最小構成の `index.html`, `style.css`, `script.js` を生成。
- 競合の良い実装例を反映し、CTA/導線/計測を組み込む。

終了時チェック（前 STEP: STEP 6）
- `PROJECT_DIR/04_lp-requirements.md` が存在すること。
- 同ファイルに TODO マーカーが残っていないこと（Windows 例）:
```bash
findstr /n "TODO" %PROJECT_DIR%\04_lp-requirements.md
```

STEP 8. 進捗と品質チェック
```bash
python -X utf8 src/workflows/check-progress.py
```
評価基準:
- `input/project-config.yaml > quality_control.required_completion_rate` を満たすこと。
- 必須レビューポイント（`quality_control.mandatory_reviews`）に沿って不足があれば追記。

終了時チェック（前 STEP: STEP 7）
- `PROJECT_DIR/lp-files/` が存在し、最低限のファイル（`index.html`, `style.css`, `script.js`）が揃っていること。
- （適用可能な場合）前 STEP の TODO マーカーが残っていないこと。

重要な注意点
- 設定ファイル依存: 各 STEP で必ず設定ファイルの情報を参照する（企業名・業界・地域情報を動的に取得）
- 業界対応: 設定された業界に応じた分析観点を追加する
- TODO マーカー更新: すべての `<!-- TODO_... -->` を実内容に更新し、前の STEP の成果を次の STEP で参照する
- 品質保証: 最終的に公開可能な品質まで仕上げる（実装可能で具体的な推奨事項を含める）

設定ファイルの活用方法
- 企業情報: `config.get_company_info()`
- 業界情報: `config.get_industry_info()`
- 競合情報: `config.get_competitors_info()`
- SEO設定: `config.get_seo_config()`
- ターゲット顧客: `config.get_target_customers()`
- マーケティング目標: `config.get_marketing_goals()`
- LP設定: `config.get_landing_page_config()`

エラー時/分岐の扱い
- 未来日付のフォルダがあると最新判定がずれるため、一時退避してから進捗チェックを実行。
- ネットワーク取得失敗時は既存サマリのみで分析を続行。
- 競合URL未設定の場合は該当箇所をスキップし、後段の TODO は残す。

完了条件
- `PROJECT_DIR/*.md` の TODO マーカーが閾値以下（可能ならゼロ）。
- `knowledge/company-info.md` と成果物間で不整合がない。
- `quality_control` の基準を満たす。

期待する成果物（必須）
- `01_competitor-analysis.md` - 業界特化の詳細競合分析
- `02_seo-analysis.md` - ターゲット地域・業界のSEO戦略
- `03_marketing-strategy.md` - 企業固有のマーケティング戦略
- `04_lp-requirements.md` - 実装可能なLP要件定義
- `05_lp-completion-report.md` - LP完成レポート
- `lp-files/` - 即座に公開可能なLP（HTML/CSS/JS）

進捗確認コマンド
```bash
# 進捗確認
python -X utf8 src/workflows/check-progress.py

# TODO マーカー残存確認（Windows）
findstr /n "TODO" output\YYYYMMDD\*.md

# 設定情報確認
python src/workflows/config_loader.py
```

成功のポイント
1. 設定ファイル活用: 汎用的な設定を活用して企業・業界に特化した分析を実行
2. 具体性: 抽象的でなく、具体的な数値・データを含める
3. 一貫性: 全STEPを通じて一貫した戦略を維持
4. 実用性: 実際に使用可能な成果物を作成
5. 品質: 妥協せず、最高品質を追求
6. 業界適応: 設定された業界に適した分析・戦略を実行

トラブルシューティング

設定ファイルが見つからない場合
```bash
# 設定ファイルテンプレートを作成（必要に応じて）
mkdir input
copy input\project-config.yaml.template input\project-config.yaml
# 企業・業界情報を記入してください
```

設定情報が不完全な場合
- `input/project-config.yaml` を編集
- 必須項目をすべて記入
- `python src/workflows/config_loader.py` で確認

プロジェクトが作成されない場合
```bash
# 手動でディレクトリ作成
mkdir output
python src/workflows/setup-project.py
```

備考
- 本プロンプトは Cursor 上での自動連鎖実行を想定しています。各STEPでは直前の成果物を必ず読み込み、差分だけを安全に書き戻してください。
- 端末操作が必要な箇所は、対話不要のフラグ（例: `--force`）を付けて実行してください。



