import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import FAQ_PATH

CHUNK_SIZE = 600
CHUNK_OVERLAP = 100
RETRIEVER_K = 4

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


@st.cache_resource
def build_vectorstore() -> InMemoryVectorStore:
    with open(FAQ_PATH, encoding="utf-8") as f:
        raw_text = f.read()

    splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", "。", "、", " ", ""],
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    docs = splitter.create_documents([raw_text])

    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    return InMemoryVectorStore.from_documents(documents=docs, embedding=embeddings)


def build_rag_chain(vectorstore: InMemoryVectorStore):
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
