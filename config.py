import os

import streamlit as st
from dotenv import load_dotenv

load_dotenv()


def get_secret(key: str, default: str = "") -> str:
    """os.environ -> st.secrets の順で値を探す。どちらにも無ければ default を返す。"""
    val = os.environ.get(key, "")
    if val:
        return val
    try:
        return st.secrets[key]
    except (KeyError, FileNotFoundError):
        return default


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

LINE_URL = get_secret("HELLOAI_LINE_URL", "https://lin.ee/vo4MyqI")
INSTAGRAM_URL = get_secret("HELLOAI_INSTAGRAM_URL", "https://www.instagram.com/hello_ai_utokyo/")
X_URL = get_secret("HELLOAI_X_URL", "https://x.com/Hello_AI_todai")
INFO_SESSION_TEXT = get_secret(
    "HELLOAI_INFO_SESSION_TEXT",
    "説明会情報はここに表示できます。実際の日時・場所・申込方法に差し替えてください。",
)
LINE_QR_PATH = get_secret("HELLOAI_LINE_QR_PATH", "")

QUESTION_CATEGORIES = [
    "入会・登録",
    "イベント",
    "活動内容",
    "技術・学習",
    "運営・連絡先",
    "その他",
]

NO_FAQ_MARKER = "FAQに見つかりませんでした"
