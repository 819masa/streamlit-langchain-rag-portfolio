import os

import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

FAQ_PATH = "faq_data.txt"
APP_NAME = "Hello AI! Q&Aボット"
APP_SUBTITLE = "Hello AI の疑問をすぐ解決できる、サークルメンバー開発のAIチャットボット"
PRIMARY_COLOR = "#003059"
SECONDARY_COLOR = "#335C81"
ACCENT_COLOR = "#669BBC"
SOFT_BG = "#F7FAFC"

SAMPLE_QUESTIONS = [
    "Hello AIでは何が学べますか？",
    "初心者でも参加できますか？",
    "入会方法を教えてください",
]

LINE_URL = os.getenv("HELLOAI_LINE_URL", "")
INSTAGRAM_URL = os.getenv("HELLOAI_INSTAGRAM_URL", "")
X_URL = os.getenv("HELLOAI_X_URL", "")
INFO_SESSION_TEXT = os.getenv(
    "HELLOAI_INFO_SESSION_TEXT",
    "説明会情報はここに表示できます。実際の日時・場所・申込方法に差し替えてください。",
)
LINE_QR_PATH = os.getenv("HELLOAI_LINE_QR_PATH", "")


def inject_custom_css() -> None:
    st.markdown(
        f"""
        <style>
        .stApp {{
            background:
                radial-gradient(circle at top, rgba(102, 155, 188, 0.18), transparent 35%),
                linear-gradient(180deg, #ffffff 0%, {SOFT_BG} 100%);
        }}

        .block-container {{
            max-width: 760px;
            padding-top: 1.25rem;
            padding-bottom: 5rem;
        }}

        h1, h2, h3, p, div, span, label {{
            font-family: "Inter", "Noto Sans JP", "Hiragino Kaku Gothic ProN", sans-serif;
        }}

        .hero-card {{
            background: linear-gradient(135deg, {PRIMARY_COLOR} 0%, {SECONDARY_COLOR} 100%);
            color: white;
            border-radius: 24px;
            padding: 1.4rem 1.25rem;
            box-shadow: 0 18px 40px rgba(0, 48, 89, 0.18);
            margin-bottom: 1rem;
        }}

        .hero-badge {{
            display: inline-block;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.02em;
            color: {PRIMARY_COLOR};
            background: rgba(255, 255, 255, 0.92);
            border-radius: 999px;
            padding: 0.3rem 0.7rem;
            margin-bottom: 0.8rem;
        }}

        .hero-title {{
            font-size: 1.95rem;
            line-height: 1.2;
            font-weight: 800;
            margin: 0 0 0.55rem 0;
        }}

        .hero-copy {{
            margin: 0;
            font-size: 0.98rem;
            line-height: 1.7;
            color: rgba(255, 255, 255, 0.92);
        }}

        .section-label {{
            color: {PRIMARY_COLOR};
            font-weight: 800;
            font-size: 0.95rem;
            margin: 1rem 0 0.35rem 0;
        }}

        .join-card {{
            background: rgba(255, 255, 255, 0.95);
            border: 1px solid rgba(0, 48, 89, 0.08);
            border-radius: 22px;
            padding: 1rem 1rem 0.65rem 1rem;
            box-shadow: 0 14px 32px rgba(0, 48, 89, 0.08);
            margin-top: 1rem;
        }}

        .join-title {{
            color: {PRIMARY_COLOR};
            font-size: 1.05rem;
            font-weight: 800;
            margin-bottom: 0.35rem;
        }}

        .join-copy {{
            color: #4b5563;
            font-size: 0.92rem;
            line-height: 1.65;
            margin-bottom: 0.85rem;
        }}

        div[data-testid="stBottomBlockContainer"] {{
            background: transparent !important;
        }}

        div[data-testid="stBottomBlockContainer"] > div {{
            background: transparent !important;
        }}

        div[data-testid="stChatFloatingInputContainer"] {{
            background: transparent !important;
        }}

        div[data-testid="stChatInput"] {{
            background: rgba(255, 255, 255, 0.98);
            border: 1px solid rgba(0, 48, 89, 0.10);
            border-radius: 18px;
            box-shadow: 0 10px 26px rgba(0, 48, 89, 0.08);
            padding-left: 0.2rem;
        }}

        div[data-testid="stChatInput"]:focus-within {{
            border: 1px solid rgba(0, 48, 89, 0.18);
            box-shadow: 0 12px 30px rgba(0, 48, 89, 0.12);
        }}

        div[data-testid="stChatInput"] textarea {{
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
        }}

        div[data-testid="stChatInput"] button {{
            background: {PRIMARY_COLOR} !important;
            color: white !important;
        }}

        div[data-testid="stChatMessage"] {{
            border-radius: 20px;
        }}

        div[data-testid="stVerticalBlock"] div.stButton > button {{
            width: 100%;
            border-radius: 16px;
            border: 1px solid rgba(0, 48, 89, 0.10);
            background: rgba(255, 255, 255, 0.96);
            color: {PRIMARY_COLOR};
            font-weight: 700;
            padding: 0.75rem 0.85rem;
            box-shadow: 0 8px 20px rgba(0, 48, 89, 0.05);
        }}

        div[data-testid="stVerticalBlock"] div.stButton > button:hover {{
            border-color: rgba(0, 48, 89, 0.20);
            color: {PRIMARY_COLOR};
        }}

        div.stLinkButton > a {{
            width: 100%;
            border-radius: 14px;
            border: 1px solid rgba(0, 48, 89, 0.10);
            background: white;
            color: {PRIMARY_COLOR};
            font-weight: 700;
        }}

        @media (max-width: 640px) {{
            .block-container {{
                padding-left: 0.95rem;
                padding-right: 0.95rem;
            }}

            .hero-title {{
                font-size: 1.65rem;
            }}

            .hero-card {{
                padding: 1.1rem 1rem;
                border-radius: 20px;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


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


def format_docs(docs) -> str:
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


def render_header() -> None:
    st.markdown(
        f"""
        <div class="hero-card">
            <div class="hero-badge">Student-built AI Assistant</div>
            <div class="hero-title">{APP_NAME}</div>
            <p class="hero-copy">{APP_SUBTITLE}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_quick_questions() -> str | None:
    st.markdown('<div class="section-label">よくある質問からすぐ聞く</div>', unsafe_allow_html=True)

    selected_question = None
    for idx, question in enumerate(SAMPLE_QUESTIONS):
        if st.button(question, key=f"sample-question-{idx}", use_container_width=True):
            selected_question = question
    return selected_question


def render_join_section() -> None:
    st.markdown(
        """
        <div class="join-card">
            <div class="join-title">入会・説明会の案内</div>
            <div class="join-copy">
                興味を持ったら、SNSやLINEから気軽にチェックしてください。説明会情報もここにまとめています。
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if LINE_QR_PATH and os.path.exists(LINE_QR_PATH):
        st.image(LINE_QR_PATH, caption="LINE登録用QR", use_container_width=True)

    if LINE_URL:
        st.link_button("LINEで問い合わせる", LINE_URL, use_container_width=True)
    else:
        st.caption("`HELLOAI_LINE_URL` を設定するとLINE導線を表示できます。")

    social_cols = st.columns(2)
    with social_cols[0]:
        if INSTAGRAM_URL:
            st.link_button("Instagram", INSTAGRAM_URL, use_container_width=True)
        else:
            st.caption("Instagram URL 未設定")
    with social_cols[1]:
        if X_URL:
            st.link_button("X", X_URL, use_container_width=True)
        else:
            st.caption("X URL 未設定")

    st.markdown('<div class="section-label">説明会情報</div>', unsafe_allow_html=True)
    st.info(INFO_SESSION_TEXT)


def run_chat_turn(question: str, rag_chain) -> None:
    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("回答を生成中..."):
            try:
                answer = rag_chain.invoke(question)
            except Exception:
                answer = "一時的に回答の生成に失敗しました。時間をおいてもう一度お試しください。"
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})


def main():
    st.set_page_config(
        page_title=APP_NAME,
        page_icon="💬",
        layout="centered",
    )

    inject_custom_css()
    render_header()

    if not os.getenv("GOOGLE_API_KEY"):
        st.error("`.env` に `GOOGLE_API_KEY` を設定してください。")
        st.stop()

    vectorstore = build_vectorstore()
    rag_chain = build_rag_chain(vectorstore)

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "こんにちは！Hello AI! に関することなら何でも聞いてください。"}
        ]

    render_join_section()
    selected_question = render_quick_questions()

    st.markdown('<div class="section-label">チャットで相談する</div>', unsafe_allow_html=True)

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("気になることを入力してください")
    question = selected_question or user_input

    if question:
        run_chat_turn(question, rag_chain)


if __name__ == "__main__":
    main()
