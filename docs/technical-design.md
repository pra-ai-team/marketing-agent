# 技術設計書（Technical Design）

## 1. アーキテクチャ概要
- CLI 実行: `src/run.py` → `src/workflows/setup-project.py`
  - `run.py` は既定で `--outdir output` を付与して `setup-project.py` を起動
- 設定読み込み: `src/workflows/config_loader.py`
- ユーザー入力反映: `src/workflows/user_input_parser.py`
- 出力: `output/YYYYMMDD/`（テンプレートMD、knowledge、競合収集物、プロジェクトREADME）

## 2. データフロー
1. `user_input.md` の検出（省略可 / `--no-user-input` でスキップ）
2. `apply_user_input_to_config(user_input.md, input/project-config.yaml)` を実行
3. `ConfigLoader` が `project-config.yaml` を読み込み
4. 出力先基底（`--outdir`、既定は `output`）配下に日付ディレクトリを作成
5. テンプレートコピー（`src/templates/generic/*.md`）
6. 競合サイト収集（robots.txt を確認し許可時のみGET）→ HTML保存と要約Markdown生成 → `competitors/summary.md` 集約
7. TODOマーカー更新（実行日時・企業名・業界名・旧テンプレ互換置換）
8. 動的知識ベース生成（`knowledge/company-info.md`）とプロジェクトサマリー生成（`project-summary.md`）
9. プロジェクトREADME生成（`README.md`）
10. 要件定義（`04_lp-requirements.md`）に競合分析ガイドを自動注入（`--no-inject` でスキップ）

## 3. モジュール構成
- `run.py`: 実行ラッパー。`workflows/setup-project.py` を呼び出し
- `workflows/setup-project.py`: メインフローとCLI引数定義
- `workflows/config_loader.py`: YAML設定の読み込み/検証/サマリ/知識生成
- `workflows/user_input_parser.py`: Markdown入力の解析とYAMLへのディープマージ
  
（補助ユーティリティ）
- `workflows/check-progress.py`: TODOマーカー残存を集計し完了率を出力
- `workflows/check-system-date.py`: システム日付の診断
- `workflows/fix-date-mismatch.py`: フォルダ日付とファイル内実行日時の不一致を修正

## 4. `user_input_parser.py` 詳細
- 入力: Markdown（`### 1-1.` などのセクション見出し、`ここに入力` 行）
- 解析: 正規表現で項目抽出、空/プレースホルダは無視
- 出力: `project-config.yaml` 互換の辞書断片
- マージ: 既存 `project-config.yaml` に対してディープマージ、配列は上書き（key_features, target_companies など）

### 4.1 主要関数
- `apply_user_input_to_config(md_path, yaml_path) -> (applied: bool, updated: List[str])`
- 内部で `_parse_user_input_markdown` と `_deep_merge` を使用

### 4.2 正規化ポリシー
- `ここに入力`、空文字、例示（例：...）は無視
- URL/カテゴリ等はそのまま格納（最低限のトリムのみ）

## 5. 例外処理・リカバリ
- `user_input.md` 不在/空: 反映スキップ、従来どおり続行
- `project-config.yaml` 読み込み失敗: 空設定として再生成
- ネットワーク失敗: 競合収集は警告のみで続行
 - Quickモード（`--quick`）: 必須検証を緩和（企業名以外の不足は警告化）。企業名は `--company` または `--company-file` で指定可能

## 6. CLI 引数
- `--date YYYYMMDD`: プロジェクト日付を指定
- `--config PATH`: 設定ファイルパス（既定: `input/project-config.yaml`）
- `--outdir PATH`: 出力先の基底ディレクトリ（既定: `output`）
- `--force`: 既存ディレクトリがあっても確認なしで続行
- `--no-competitors`: 競合サイトの自動取得をスキップ
- `--no-inject`: `04_lp-requirements.md` への競合分析ガイド注入をスキップ
- `--fetch-timeout INT`: 競合サイト取得のHTTPタイムアウト（秒）
- `--max-competitors INT`: 取得対象の上限件数（未指定なら全件）
- `--quick`: 不足設定を警告に緩和（企業名のみ必須）
- `--company NAME`: 企業名を直接指定（`--quick` と併用推奨）
- `--company-file PATH`: 企業名を1行で記載したファイルパス（既定: `input/company-name.txt`）
- `--no-user-input`: `user_input.md` の反映をスキップ

## 7. 将来拡張
- 差分プレビュー（反映前に更新予定キーを表示）
- YAML スキーマ強化と型検証
- 自動業界推定/競合抽出の外部API連携
