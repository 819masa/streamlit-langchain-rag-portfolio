# Hello AI! Q&Aボット

新入生向けの RAG（Retrieval-Augmented Generation）チャットボット。Hello AI! に関する FAQ をもとに、AI が質問に即座に回答します。

**公開 URL**: [https://hello-ai-question-and-answer-bot.streamlit.app/](https://hello-ai-question-and-answer-bot.streamlit.app/)

## 技術スタック

| カテゴリ | 技術 |
|---|---|
| 言語 | Python |
| UI | Streamlit |
| LLM | Google Gemini 2.0 Flash |
| 埋め込みモデル | Gemini Embedding 001 |
| フレームワーク | LangChain (LCEL) |
| ベクトルストア | LangChain InMemoryVectorStore |
| 質問ログ DB | Supabase (PostgreSQL) |
| デプロイ | Streamlit Community Cloud |

## アーキテクチャ

```
ユーザー
  ↓ 質問
Streamlit UI
  ↓
LangChain LCEL Chain
  ├─ Retriever（InMemoryVectorStore ← FAQ テキスト）
  ├─ Gemini 2.0 Flash（回答生成）
  └─ Gemini（質問カテゴリ自動分類）
        ↓
Supabase（質問・回答・カテゴリをログ保存）
```

1. **起動時**: `faq_data.txt` を `RecursiveCharacterTextSplitter` でチャンク分割 → Gemini Embeddings でベクトル化 → インメモリストアに保持
2. **質問時**: Retriever で関連チャンクを検索 → コンテキスト + 質問を Gemini に渡して回答生成
3. **ログ**: 質問を Gemini でカテゴリ分類し、Supabase に保存（FAQ 改善ループ用）

## ローカル開発

```bash
# 1. リポジトリをクローン
git clone https://github.com/<your-username>/streamlit-langchain-rag-portfolio.git
cd streamlit-langchain-rag-portfolio

# 2. 仮想環境を作成・有効化
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux

# 3. 依存パッケージをインストール
pip install -r requirements.txt

# 4. 環境変数を設定
copy .env.example .env        # Windows
# cp .env.example .env        # macOS / Linux
# .env を開いて各キーを入力

# 5. (任意) Supabase のテーブルを作成
# Supabase SQL Editor で supabase_setup.sql を実行

# 6. 起動
streamlit run app.py --server.port 8504 --server.fileWatcherType none
```

ブラウザで `http://localhost:8504` を開いてください。

> Windows では `--server.fileWatcherType none` を付けると、Streamlit がすぐ終了する問題を回避できます。

## Streamlit Community Cloud へのデプロイ

1. GitHub にリポジトリを push する
2. [share.streamlit.io](https://share.streamlit.io) でアプリを作成
3. **Settings → Secrets** に以下を TOML 形式で入力:

```toml
GOOGLE_API_KEY = "your_google_api_key"
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_ANON_KEY = "your_supabase_anon_key"
```

## ファイル構成

```
├── app.py                 # メインアプリケーション
├── faq_data.txt           # FAQ データソース
├── requirements.txt       # Python 依存パッケージ
├── supabase_setup.sql     # Supabase テーブル定義
├── .env.example           # 環境変数テンプレート
├── .streamlit/
│   └── config.toml        # Streamlit テーマ設定（ライトモード強制）
├── TODO.md                # 今後の改善計画
└── README.md
```
