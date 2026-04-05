import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import FAQ_PATH
from chain import CHUNK_SIZE, CHUNK_OVERLAP, RETRIEVER_K, SYSTEM_PROMPT, _format_docs


def test_chunk_params_are_reasonable():
    assert 200 <= CHUNK_SIZE <= 2000, f"chunk_size={CHUNK_SIZE} は範囲外"
    assert 0 < CHUNK_OVERLAP < CHUNK_SIZE, "chunk_overlap は 0 < overlap < chunk_size"
    assert 1 <= RETRIEVER_K <= 10, f"k={RETRIEVER_K} は範囲外"


def test_system_prompt_contains_context_placeholder():
    assert "{context}" in SYSTEM_PROMPT


def test_system_prompt_mentions_faq_not_found():
    assert "FAQ" in SYSTEM_PROMPT


def test_splitter_produces_chunks():
    with open(FAQ_PATH, encoding="utf-8") as f:
        raw_text = f.read()

    splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", "。", "、", " ", ""],
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    docs = splitter.create_documents([raw_text])

    assert len(docs) >= 3, f"チャンク数が少なすぎます: {len(docs)}"
    for doc in docs:
        assert len(doc.page_content) <= CHUNK_SIZE + 200, (
            f"チャンクが大きすぎます: {len(doc.page_content)} chars"
        )


def test_format_docs():
    class FakeDoc:
        def __init__(self, text):
            self.page_content = text

    docs = [FakeDoc("aaa"), FakeDoc("bbb"), FakeDoc("ccc")]
    result = _format_docs(docs)
    assert "aaa" in result
    assert "bbb" in result
    assert "---" in result
