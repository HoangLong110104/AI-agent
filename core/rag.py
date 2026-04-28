from core.embedding import APIEmbedding
from core.chroma_utils import get_chroma
from config import EMBEDDING_ENABLED

def keyword_score(q, doc):
    q = q.lower().split()
    d = doc.lower()
    return sum(1 for w in q if w in d) / len(q) if q else 0

def hybrid_search(query, topk=3):
    if not EMBEDDING_ENABLED:
        return []

    client = get_chroma()
    embedder = APIEmbedding()
    qemb = embedder.embed([query])[0]

    results = []
    for col in client.list_collections():
        c = client.get_collection(col.name)
        r = c.query(
            query_embeddings=[qemb],
            n_results=10,
            include=["documents", "distances"]
        )
        for doc, dist in zip(r["documents"][0], r["distances"][0]):
            sem = 1 - dist
            kw = keyword_score(query, doc)
            score = 0.7 * sem + 0.3 * kw
            results.append((score, doc))

    results.sort(key=lambda x: x[0], reverse=True)
    return [x[1] for x in results[:topk]]