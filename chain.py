import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.vectorstores import SupabaseVectorStore

from config import get_secret
from db import get_supabase

EMBEDDING_MODEL = "models/gemini-embedding-001"
EMBEDDING_DIMS = 768
RETRIEVER_K = 4
TABLE_NAME = "documents"
QUERY_NAME = "match_documents"

SYSTEM_PROMPT = (
    "あなたは Hello AI! のFAQサポートBotです。\n"
    "以下の【参考情報】だけを根拠にして、ユーザーの質問に丁寧かつ簡潔に日本語で回答してください。\n"
    "- 箇条書きや番号付きリストを活用して読みやすくしてください。\n"
    "- 参考情報に答えが無い場合は「申し訳ありませんが、その質問に関する情報はFAQに見つかりませんでした。」と回答してください。\n"
    "- 参考情報に無い内容を推測で補わないでください。\n\n"
    "【参考情報】\n{context}"
)


def _format_docs(docs) -> str:
    return "\n\n---\n\n".join(doc.page_content for doc in docs)


def _get_embeddings() -> GoogleGenerativeAIEmbeddings:
    return GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        task_type="retrieval_query",
    )


@st.cache_resource
def build_vectorstore() -> SupabaseVectorStore:
    sb = get_supabase()
    if sb is None:
        st.error("Supabase に接続できません。環境変数を確認してください。")
        st.stop()

    return SupabaseVectorStore(
        client=sb,
        embedding=_get_embeddings(),
        table_name=TABLE_NAME,
        query_name=QUERY_NAME,
    )


def build_rag_chain(vectorstore: SupabaseVectorStore):
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)
    retriever = vectorstore.as_retriever(search_kwargs={"k": RETRIEVER_K})

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{question}"),
    ])

    return (
        {"context": retriever | _format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
