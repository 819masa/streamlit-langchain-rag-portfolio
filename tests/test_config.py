import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from config import (
    APP_NAME,
    FAQ_PATH,
    QUESTION_CATEGORIES,
    NO_FAQ_MARKER,
    SAMPLE_QUESTIONS,
    PRIMARY_COLOR,
)


def test_app_name_is_set():
    assert APP_NAME
    assert "Hello AI" in APP_NAME


def test_faq_path_exists():
    assert os.path.isfile(FAQ_PATH), f"{FAQ_PATH} が見つかりません"


def test_faq_file_is_utf8():
    with open(FAQ_PATH, encoding="utf-8") as f:
        content = f.read()
    assert len(content) > 100, "FAQ データが短すぎます"


def test_question_categories_not_empty():
    assert len(QUESTION_CATEGORIES) >= 3
    assert "その他" in QUESTION_CATEGORIES


def test_sample_questions_not_empty():
    assert len(SAMPLE_QUESTIONS) >= 1
    for q in SAMPLE_QUESTIONS:
        assert isinstance(q, str)
        assert len(q) > 0


def test_no_faq_marker_present():
    assert NO_FAQ_MARKER
    assert isinstance(NO_FAQ_MARKER, str)


def test_primary_color_is_hex():
    assert PRIMARY_COLOR.startswith("#")
    assert len(PRIMARY_COLOR) == 7
