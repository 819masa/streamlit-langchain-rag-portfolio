import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import FAQ_PATH
from chain import RETRIEVER_K, SYSTEM_PROMPT, _format_docs, EMBEDDING_DIMS


def test_retriever_k_is_reasonable():
    assert 1 <= RETRIEVER_K <= 10, f"k={RETRIEVER_K} は範囲外"


def test_embedding_dims_is_valid():
    assert EMBEDDING_DIMS in (256, 512, 768, 1536, 3072)


def test_system_prompt_contains_context_placeholder():
    assert "{context}" in SYSTEM_PROMPT


def test_system_prompt_mentions_faq_not_found():
    assert "FAQ" in SYSTEM_PROMPT


def test_splitter_produces_chunks():
    """reindex.py と同じパラメータでチャンク分割が正常に動くことを確認"""
    chunk_size = 600
    chunk_overlap = 100

    with open(FAQ_PATH, encoding="utf-8") as f:
        raw_text = f.read()

    splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", "。", "、", " ", ""],
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    docs = splitter.create_documents([raw_text])

    assert len(docs) >= 3, f"チャンク数が少なすぎます: {len(docs)}"
    for doc in docs:
        assert len(doc.page_content) <= chunk_size + 200, (
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
