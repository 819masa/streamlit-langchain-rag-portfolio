# CloudFlow 社内FAQ サポートBot

RAG（Retrieval-Augmented Generation）を活用した社内FAQチャットボットのポートフォリオプロジェクトです。

## 技術スタック

| カテゴリ | 技術 |
|---|---|
| 言語 | Python |
| UI | Streamlit |
| LLM | OpenAI GPT-4o-mini |
| 埋め込みモデル | text-embedding-3-small |
| フレームワーク | LangChain (LCEL) |
| ベクトルDB | ChromaDB |

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
# .env ファイルを開き、OPENAI_API_KEY に自分のAPIキーを設定
```

## 起動方法

```bash
streamlit run app.py
```

ブラウザで `http://localhost:8501` が自動的に開きます。

## ファイル構成

```
├── app.py              # メインアプリケーション
├── faq_data.txt        # FAQデータソース
├── requirements.txt    # Python依存パッケージ
├── .env                # 環境変数（APIキー）
└── README.md
```

## アーキテクチャ

1. **データ読み込み**: `faq_data.txt` を `CharacterTextSplitter` でチャンクに分割
2. **ベクトル化**: OpenAI Embeddings でベクトル化し ChromaDB に保存
3. **検索**: ユーザーの質問に類似するチャンクを Retriever で取得
4. **回答生成**: 取得したコンテキストと質問を GPT-4o-mini に渡し、回答を生成
