# 要件定義書（Requirements Specification）

## 1. 目的
本ツールは、ユーザー入力（`user_input.md`）と設定（`input/project-config.yaml`）を基に、
競合分析、SEO分析、マーケティング戦略立案、LP要件定義、LP雛形生成までを自動化・半自動化する。

## 2. スコープ
- 入力: `user_input.md`（必須最小: 企業名・地域）/ `project-config.yaml`
- 出力: `output/YYYYMMDD/` 配下の分析ドキュメント一式と `knowledge/company-info.md`
- 競合サイトの自動収集（robots.txt を尊重）
- 要件定義への競合ガイド自動注入
 - プロジェクトREADMEとプロジェクトサマリーの自動生成

## 3. 関係者
- ユーザー（事業担当/制作担当）
- 開発者（本ツールの保守者）

## 4. 用語
- Quick 実行: 最小入力（企業名・地域）で走らせる実行モード
- 設定ファイル: `input/project-config.yaml`

## 5. 前提・制約
- OS: Windows 10/11、Python 3.8+
- 外部ネットワークアクセス: 競合サイト収集に使用（遮断時はスキップ）
- 生成物はローカル出力を前提

## 6. 機能要件
- FR-1: `user_input.md` の解析と `project-config.yaml` への反映
- FR-2: 設定の妥当性チェック（企業名・地域の必須検証、他は警告）
- FR-3: 汎用テンプレートのコピー（01〜05の各Markdown）
- FR-4: 競合サイト自動収集と要約の保存
- FR-5: TODOマーカーの自動更新（実行日時・企業名・業界名）
- FR-6: 動的知識ベースの生成（`knowledge/company-info.md`）
- FR-7: プロジェクトREADMEの生成（作業手順・品質チェック含む）
- FR-8: プロジェクトサマリーの生成（`project-summary.md`）
- FR-9: 要件定義への競合分析ガイドの自動注入

## 7. 非機能要件
- NFR-1: 実行時間は一般的なネットワーク環境で10分以内（競合取得件数に依存）
- NFR-2: ログは標準出力で日本語メッセージを表示
- NFR-3: 失敗時は分岐ごとに明確な警告/エラーメッセージを出力

## 8. 入出力
- 入力: `user_input.md`, `input/project-config.yaml`（存在すれば）
- 出力: `output/YYYYMMDD/` 以下に Markdown/HTML/CSS/JS（`knowledge/`, `competitors/` を含む）

## 9. 例外・エラー処理
- `user_input.md` 不在: 情報反映をスキップして続行
- `project-config.yaml` 不在: Quick モードでは空設定から開始
- ネットワークエラー: 競合収集は警告のみで続行
- Quick モード: 企業名以外の不足は警告化。企業名は `--company` または `--company-file` で指定可能

## 10. セキュリティ
- 外部取得時は robots.txt を尊重
- 収集したHTMLはローカル保存のみ

## 11. 今後の拡張
- SERP連携でのキーワード候補自動収集
- LP自動生成のデザインテンプレート拡充
- プロンプト駆動の逐次レビュー自動化
 
