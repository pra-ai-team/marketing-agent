# CAD AI Creator

店舗設計に特化したスクリプトベースの2D CADアプリケーション。Pythonスクリプトによる図面操作、AI連携による自然言語処理、既存CADファイルのインポート機能を提供します。

## 機能

### 実装済み機能
- **基本的な2D図形レンダリング**: Canvas APIとFabric.jsを使用した図形描画
- **Pythonスクリプトエンジン**: PyScript/Pyodideによる安全なスクリプト実行環境
- **店舗構造描画**: 壁、柱、出入口の描画コマンド
- **什器・設備配置**: 棚、レジ、設備の配置コマンド
- **図形編集機能**: 移動、削除、複製、ラベル追加
- **スクリプトエディタ**: シンタックスハイライト、エラー表示、実行機能
- **インタラクティブキャンバス**: ズーム、パン、図形選択機能

### 利用可能なスクリプトコマンド
- `cad.draw_wall(start, end, thickness)` - 壁の描画
- `cad.draw_column(center, width, height, shape_type)` - 柱の描画
- `cad.draw_door(position, width, direction)` - 出入口の描画
- `cad.place_fixture(position, width, height, fixture_type)` - 什器の配置
- `cad.place_equipment(position, width, height, equipment_type)` - 設備の配置
- `cad.create_area(vertices, area_type)` - エリアの作成
- `cad.move_shape(shape_id, delta_x, delta_y)` - 図形の移動
- `cad.delete_shape(shape_id)` - 図形の削除
- `cad.copy_shape(shape_id, offset_x, offset_y)` - 図形の複製
- `cad.add_label(shape_id, text)` - ラベルの追加

## 技術スタック

### フロントエンド
- React + TypeScript
- Fabric.js (Canvas操作)
- PyScript/Pyodide (Python実行環境)
- Vite (ビルドツール)

### バックエンド
- Node.js + Express
- TypeScript
- CORS、Helmet (セキュリティ)
- Rate Limiting

## セットアップ

### 前提条件
- Node.js 18.0.0以上
- npm または yarn

### インストール

1. リポジトリをクローン:
```bash
git clone <repository-url>
cd cad-ai-creator
```

2. 依存関係をインストール:
```bash
# クライアント
cd client
npm install

# サーバー
cd ../server
npm install
```

### 開発サーバーの起動

1. クライアント (http://localhost:5173):
```bash
cd client
npm run dev
```

2. サーバー (http://localhost:3001):
```bash
cd server
npm run dev
```

## 使用方法

### 基本的な使用方法

1. アプリケーションを起動
2. 左側のスクリプトエディタにPythonコードを入力
3. "Execute"ボタンをクリックして実行
4. 右側のキャンバスで結果を確認

### サンプルスクリプト

```python
# 店舗の基本構造を作成
cad.draw_wall((0, 0), (2000, 0), 100)      # 前面の壁
cad.draw_wall((2000, 0), (2000, 1500), 100) # 右側の壁
cad.draw_wall((2000, 1500), (0, 1500), 100) # 背面の壁
cad.draw_wall((0, 1500), (0, 0), 100)      # 左側の壁

# 入口を追加
cad.draw_door((900, 0), 800, "right")

# レジカウンターを配置
cad.place_fixture((200, 200), 400, 100, "checkout counter")

# 棚を配置
cad.place_fixture((800, 400), 300, 100, "shelf")

# 在庫エリアを作成
cad.create_area([(1600, 1000), (1900, 1000), (1900, 1400), (1600, 1400)], "storage")
```

### キャンバス操作

- **パン**: Shift + ドラッグ
- **ズーム**: マウスホイール
- **座標取得**: ダブルクリック
- **図形選択**: 図形をクリック

## プロジェクト構造

```
cad-ai-creator/
├── client/                 # フロントエンド
│   ├── src/
│   │   ├── components/     # Reactコンポーネント
│   │   ├── services/       # ビジネスロジック
│   │   ├── types/          # 型定義
│   │   └── utils/          # ユーティリティ
│   ├── package.json
│   └── vite.config.ts
├── server/                 # バックエンド
│   ├── src/
│   │   ├── controllers/    # APIコントローラー
│   │   ├── services/       # ビジネスロジック
│   │   ├── routes/         # ルーティング
│   │   ├── middleware/     # ミドルウェア
│   │   └── types/          # 型定義
│   ├── package.json
│   └── tsconfig.json
└── README.md
```

## 今後の実装予定

- AI連携による自然言語処理
- DXF/DWGファイルのインポート機能
- テンプレート管理機能
- 高度なエラーハンドリング
- ユニットテスト
- パフォーマンス最適化

## 貢献

プロジェクトへの貢献を歓迎します。以下の手順に従ってください：

1. フィーチャーブランチを作成
2. 変更を実装
3. テストを実行
4. プルリクエストを作成

## ライセンス

このプロジェクトは MIT ライセンスの下で公開されています。