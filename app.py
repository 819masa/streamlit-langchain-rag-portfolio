import os

import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

FAQ_PATH = "faq_data.txt"


@st.cache_resource
def build_vectorstore() -> InMemoryVectorStore:
    with open(FAQ_PATH, encoding="utf-8") as f:
        raw_text = f.read()

    splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", "。", "、", " ", ""],
        chunk_size=1000,
        chunk_overlap=150,
    )
    docs = splitter.create_documents([raw_text])

    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    return InMemoryVectorStore.from_documents(documents=docs, embedding=embeddings)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def build_rag_chain(vectorstore: InMemoryVectorStore):
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    system_prompt = (
        "あなたはHello AI!の社内FAQサポートBotです。"
        "以下の参考情報だけを使って、ユーザーの質問に丁寧に日本語で回答してください。"
        "参考情報に答えが無い場合は「申し訳ありませんが、その質問に関する情報はFAQに見つかりませんでした。」と回答してください。\n\n"
        "{context}"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{question}"),
    ])

    return (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )


def main():
    st.set_page_config(
        page_title="Hello AI! FAQ Bot",
        page_icon="☁️",
        layout="centered",
    )

    st.title("☁️ Hello AI! 基本情報 サポートBot")
    st.caption("Hello AI!に関する質問をどうぞ。FAQデータをもとにお答えします。")

    vectorstore = build_vectorstore()
    rag_chain = build_rag_chain(vectorstore)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "こんにちは！Hello AI!に関するご質問をどうぞ。"}
        ]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if user_input := st.chat_input("質問を入力してください…"):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("回答を生成中…"):
                answer = rag_chain.invoke(user_input)
            st.markdown(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})


if __name__ == "__main__":
    main()
