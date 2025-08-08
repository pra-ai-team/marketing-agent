## シンプル構成での使い方

構成:
- `input/` 入力（企業名・詳細設定）
- `src/`   実行
- `output/` 生成物
- `docs/`  ドキュメント

最短手順:
1. 企業名を `input/company-name.txt` に1行で記入
2. 実行
   ```bash
   python src/run.py --quick
   ```
3. 出力を確認
   - `output/YYYYMMDD/` にテンプレートと `knowledge/company-info.md` が生成

詳細設定:
- `input/project-config.yaml` を作成・編集
- 内容チェック: `python workflows/config_loader.py`（開発者向け）


