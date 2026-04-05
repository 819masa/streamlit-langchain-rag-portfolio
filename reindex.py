"""FAQ データを Supabase pgvector に再インデックスするスクリプト。

使い方:
    python reindex.py

faq_data.txt をチャンク分割 → Gemini Embeddings でベクトル化 →
Supabase の documents テーブルを全削除して新しいデータを挿入します。
"""

import os
import sys

from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import SupabaseVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from supabase import create_client

load_dotenv()

FAQ_PATH = "faq_data.txt"
CHUNK_SIZE = 600
CHUNK_OVERLAP = 100
EMBEDDING_MODEL = "models/gemini-embedding-001"
TABLE_NAME = "documents"
QUERY_NAME = "match_documents"


def main():
    url = os.environ.get("SUPABASE_URL", "")
    key = os.environ.get("SUPABASE_ANON_KEY", "")
    google_key = os.environ.get("GOOGLE_API_KEY", "")

    if not url or not key:
        print("ERROR: SUPABASE_URL / SUPABASE_ANON_KEY が .env に設定されていません")
        sys.exit(1)
    if not google_key:
        print("ERROR: GOOGLE_API_KEY が .env に設定されていません")
        sys.exit(1)

    print(f"[1/4] {FAQ_PATH} を読み込み中...")
    with open(FAQ_PATH, encoding="utf-8") as f:
        raw_text = f.read()

    print(f"[2/4] チャンク分割中 (size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})...")
    splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", "。", "、", " ", ""],
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    docs = splitter.create_documents([raw_text])
    print(f"       → {len(docs)} チャンク生成")

    sb = create_client(url, key)

    print("[3/4] 既存データを削除中...")
    sb.table(TABLE_NAME).delete().neq("id", 0).execute()
    print("       → 削除完了")

    print("[4/4] ベクトル化して Supabase に挿入中...")
    embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)

    SupabaseVectorStore.from_documents(
        documents=docs,
        embedding=embeddings,
        client=sb,
        table_name=TABLE_NAME,
        query_name=QUERY_NAME,
    )

    print(f"\n完了！ {len(docs)} チャンクを Supabase に登録しました。")


if __name__ == "__main__":
    main()
