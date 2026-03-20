# Hello AI! 社内FAQ サポートBot

RAG（Retrieval-Augmented Generation）を活用した社内FAQチャットボットのポートフォリオプロジェクトです。

## 技術スタック

| カテゴリ | 技術 |
|---|---|
| 言語 | Python |
| UI | Streamlit |
| LLM | Google Gemini 2.0 Flash |
| 埋め込みモデル | embedding-001 |
| フレームワーク | LangChain (LCEL) |
| ベクトルストア | LangChain InMemoryVectorStore |

## セットアップ

```bash
# 1. リポジトリをクローン
git clone https://github.com/<your-username>/streamlit-langchain-rag-portfolio.git
cd streamlit-langchain-rag-portfolio

# 2. 仮想環境を作成・有効化
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # macOS / Linux

# 3. 依存パッケージをインストール
pip install -r requirements.txt

# 4. 環境変数を設定
# .env ファイルを開き、GOOGLE_API_KEY に自分のAPIキーを設定
```

## 起動方法

```bash
streamlit run app.py --server.port 8504 --server.fileWatcherType none
```

ブラウザで `http://localhost:8504` を開いてください。

Windows 環境では `--server.fileWatcherType none` を付けることで、Streamlit が数秒後に終了してしまう問題を回避できます。

## ファイル構成

```
├── app.py              # メインアプリケーション
├── faq_data.txt        # FAQデータソース
├── requirements.txt    # Python依存パッケージ
├── .env                # 環境変数（APIキー）
└── README.md
```

## アーキテクチャ

1. **データ読み込み**: `faq_data.txt` を `RecursiveCharacterTextSplitter` で自然な区切りごとにチャンク分割
2. **ベクトル化**: Gemini Embeddings でベクトル化し、インメモリのベクトルストアに保持
3. **検索**: ユーザーの質問に類似するチャンクを Retriever で取得
4. **回答生成**: 取得したコンテキストと質問を Gemini 2.0 Flash に渡し、回答を生成
