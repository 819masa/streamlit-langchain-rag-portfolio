import os

import streamlit as st

from config import APP_NAME, get_secret
from chain import build_vectorstore, build_rag_chain
from db import classify_question, save_question_log
from ui import inject_custom_css, render_header, render_quick_questions, render_join_section


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

    try:
        category = classify_question(question)
        save_question_log(question, answer, category)
    except Exception:
        pass


def main():
    st.set_page_config(
        page_title=APP_NAME,
        page_icon="💬",
        layout="centered",
    )

    inject_custom_css()
    render_header()

    google_api_key = get_secret("GOOGLE_API_KEY")
    if google_api_key:
        os.environ["GOOGLE_API_KEY"] = google_api_key
    if not os.environ.get("GOOGLE_API_KEY"):
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
