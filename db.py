from datetime import datetime, timezone

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from config import get_secret, QUESTION_CATEGORIES, NO_FAQ_MARKER

_supabase_client = None


def get_supabase():
    global _supabase_client
    if _supabase_client is not None:
        return _supabase_client

    url = get_secret("SUPABASE_URL")
    key = get_secret("SUPABASE_ANON_KEY")
    if not url or not key:
        return None

    try:
        from supabase import create_client
        _supabase_client = create_client(url, key)
        return _supabase_client
    except Exception:
        return None


def classify_question(question: str) -> str:
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)
        categories_str = " / ".join(QUESTION_CATEGORIES)
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                f"以下のカテゴリの中から、ユーザーの質問に最も当てはまるカテゴリを1つだけ返してください。"
                f"カテゴリ名だけを返してください。余計な説明は不要です。\n"
                f"カテゴリ: {categories_str}",
            ),
            ("human", "{question}"),
        ])
        chain = prompt | llm | StrOutputParser()
        result = chain.invoke({"question": question}).strip()
        if result in QUESTION_CATEGORIES:
            return result
        return "その他"
    except Exception:
        return "その他"


def save_question_log(question: str, answer: str, category: str) -> None:
    sb = get_supabase()
    if sb is None:
        return

    is_in_faq = NO_FAQ_MARKER not in answer

    try:
        sb.table("question_logs").insert({
            "question": question,
            "answer": answer,
            "category": category,
            "is_in_faq": is_in_faq,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }).execute()
    except Exception:
        pass
