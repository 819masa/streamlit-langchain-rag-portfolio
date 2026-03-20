import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

FAQ_PATH = "faq_data.txt"
CHROMA_DIR = "./chroma_db"


@st.cache_resource
def build_vectorstore() -> Chroma:
    with open(FAQ_PATH, encoding="utf-8") as f:
        raw_text = f.read()

    splitter = CharacterTextSplitter(
        separator="\n\n",
        chunk_size=300,
        chunk_overlap=50,
    )
    docs = splitter.create_documents([raw_text])

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=CHROMA_DIR,
    )
    return vectorstore


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def build_rag_chain(vectorstore: Chroma):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    system_prompt = (
        "あなたはHello AI!の基本情報サポートBotです。"
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
        page_title="CloudFlow FAQ Bot",
        page_icon="☁️",
        layout="centered",
    )

    st.title("☁️ Hello AI! 基本情報 サポートBot")
    st.caption("Hello AI!に関する質問をどうぞ。FAQデータをもとにお答えします。")

    vectorstore = build_vectorstore()
    rag_chain = build_rag_chain(vectorstore)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "こんにちは！CloudFlowに関するご質問をどうぞ。"}
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
