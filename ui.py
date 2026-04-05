import os

import streamlit as st

from config import (
    APP_NAME,
    APP_SUBTITLE,
    PRIMARY_COLOR,
    SECONDARY_COLOR,
    SOFT_BG,
    SAMPLE_QUESTIONS,
    LINE_URL,
    INSTAGRAM_URL,
    X_URL,
    LINE_QR_PATH,
)


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
            transition: all 0.2s ease;
        }}

        div.stLinkButton > a:hover {{
            box-shadow: 0 8px 24px rgba(0, 48, 89, 0.12);
            transform: translateY(-1px);
        }}

        div.cta-button div.stLinkButton > a {{
            background: linear-gradient(135deg, {PRIMARY_COLOR} 0%, {SECONDARY_COLOR} 100%);
            color: white !important;
            border: none;
            font-size: 1.05rem;
            font-weight: 800;
            padding: 0.85rem 1rem;
            border-radius: 16px;
            box-shadow: 0 12px 28px rgba(0, 48, 89, 0.22);
            letter-spacing: 0.02em;
            transition: all 0.25s ease;
        }}

        div.cta-button div.stLinkButton > a:hover {{
            box-shadow: 0 16px 36px rgba(0, 48, 89, 0.32);
            transform: translateY(-2px);
            filter: brightness(1.08);
        }}

        div.cta-button div.stLinkButton > a:active {{
            transform: translateY(0px);
            box-shadow: 0 6px 16px rgba(0, 48, 89, 0.18);
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
        f"""
        <div class="join-card">
            <div class="join-title">🚀 大学生活、後悔したくないなら</div>
            <div class="join-copy">
                AIを武器にすれば、学び方も働き方も変わる。<br>
                Hello AI! は、本気で挑戦したい学生が集まる場所です。
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="join-card">
            <div class="join-title">🔥 AI解約予測コンペ</div>
            <div class="join-copy">
                実データでモデル構築に挑戦！初心者歓迎。<br>
                上位者にはインターン選考優遇も。<br>
                <strong>期間：4/13（月）〜 4/27（月）23:59</strong>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.container():
        st.markdown('<div class="cta-button">', unsafe_allow_html=True)
        st.link_button(
            "🔥 コンペに申し込む（無料）",
            "https://forms.gle/NK5DheqjLu1rGRms8",
            use_container_width=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="join-card">
            <div class="join-title">🍕 オフライン新歓＠渋谷</div>
            <div class="join-copy">
                「AIで大学生活をハックする —— 後悔しないための10の武器」<br>
                <strong>4/17（金）19:00〜 ｜ 無料食事付き！</strong><br>
                AIを使いこなして学習・効率を最大化する方法 / スタートアップが求める人材 / 交流会
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.container():
        st.markdown('<div class="cta-button">', unsafe_allow_html=True)
        st.link_button(
            "🍕 4/17の新歓イベントに参加する（1分で完了・食事付き）",
            "https://forms.gle/w6Mtshsqjq7WyhWJ8",
            use_container_width=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="join-card">
            <div class="join-title">📲 LINE・SNSをフォロー</div>
            <div class="join-copy">
                最新のイベント情報や活動報告はこちらから。気軽にフォローしてください。
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if LINE_QR_PATH and os.path.exists(LINE_QR_PATH):
        st.image(LINE_QR_PATH, caption="LINE登録用QR", use_container_width=True)

    st.link_button("LINE公式アカウントを追加", LINE_URL, use_container_width=True)

    social_cols = st.columns(2)
    with social_cols[0]:
        st.link_button("Instagram", INSTAGRAM_URL, use_container_width=True)
    with social_cols[1]:
        st.link_button("X (Twitter)", X_URL, use_container_width=True)
