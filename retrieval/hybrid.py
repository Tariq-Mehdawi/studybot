import re

from rank_bm25 import BM25Okapi

from embeddings.embedder import embed
from vectorstore.store import get_collection

RRF_K = 60

_bm25 = None
_chunk_ids = None
_chunk_texts = None


def tokenize(text):
    return re.findall(r"[a-z0-9]+", text.lower())


def get_bm25():
    """Build the keyword index once, from whatever is in Chroma."""
    global _bm25, _chunk_ids, _chunk_texts

    if _bm25 is None:
        data = get_collection().get()
        _chunk_ids = data["ids"]
        _chunk_texts = data["documents"]
        _bm25 = BM25Okapi([tokenize(t) for t in _chunk_texts])

    return _bm25, _chunk_ids, _chunk_texts


def hybrid_search(question, n_results=3, candidates=20):
    bm25, ids, texts = get_bm25()

    # --- vector search ---
    vector = embed([question])[0]
    vector_hits = get_collection().query(
        query_embeddings=[vector.tolist()],
        n_results=candidates,
    )
    vector_ranking = vector_hits["ids"][0]

    # --- keyword search ---
    scores = bm25.get_scores(tokenize(question))
    top_keyword = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
    keyword_ranking = [ids[i] for i in top_keyword[:candidates]]

    # --- reciprocal rank fusion ---
    fused = {}
    for ranking in (vector_ranking, keyword_ranking):
        for rank, chunk_id in enumerate(ranking, 1):
            fused[chunk_id] = fused.get(chunk_id, 0) + 1 / (RRF_K + rank)

    best = sorted(fused, key=fused.get, reverse=True)[:n_results]

    by_id = dict(zip(ids, texts))
    return best, [by_id[i] for i in best]