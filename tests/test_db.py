import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from config import QUESTION_CATEGORIES, NO_FAQ_MARKER


def test_no_faq_marker_detection():
    answer_with_faq = "Hello AI!は2025年5月に設立されたAIサークルです。"
    answer_without_faq = f"申し訳ありませんが、その質問に関する情報は{NO_FAQ_MARKER}。"

    assert NO_FAQ_MARKER not in answer_with_faq
    assert NO_FAQ_MARKER in answer_without_faq


def test_question_categories_are_strings():
    for cat in QUESTION_CATEGORIES:
        assert isinstance(cat, str)
        assert len(cat) > 0


def test_fallback_category_exists():
    assert "その他" in QUESTION_CATEGORIES
