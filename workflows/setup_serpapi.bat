@echo off
echo 🔧 SerpAPI キーワード分析ツール セットアップ
echo ================================================

echo.
echo 1. Python依存関係をインストール中...
pip install -r requirements.txt

echo.
echo 2. SerpAPIキーの設定
echo.
echo SerpAPIのアカウント作成手順:
echo 1. https://serpapi.com/ にアクセス
echo 2. 無料アカウント作成（月100回まで無料）
echo 3. APIキーを取得
echo.

set /p SERPAPI_KEY="取得したAPIキーを入力してください: "

if "%SERPAPI_KEY%"=="" (
    echo ❌ APIキーが入力されていません
    pause
    exit /b 1
)

echo.
echo 3. 環境変数を設定中...
setx SERPAPI_KEY "%SERPAPI_KEY%"

echo.
echo ✅ セットアップ完了！
echo.
echo 次のコマンドでキーワード分析を実行できます:
echo cd workflows
echo python seo-keyword-analyzer.py
echo.

pause 