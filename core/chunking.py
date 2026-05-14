import re
from sklearn.metrics.pairwise import cosine_similarity

def structure_aware_chunk(text):
    pattern = r"(?:^|\n)(\d+[.)]\s+[A-Z][^:\n]{2,}:)"
    parts = re.split(pattern, text)uiop

    if len(parts) >= 3:
        chunks = []
        i = 0
        while i < len(parts)-1:
            chunks.append(parts[i+1] + "\n" + parts[i+2])
            i += 2
        return chunks
    return None

def semantic_chunk(text, embedder, threshold=0.35, max_sent=10):
    sents = re.split(r"(?<=[.!?])\s+", text)
    sents = [s for s in sents if s.strip()]
    if not sents:
        return []

    embs = embedder.embed(sents)
    chunks, cur = [], [sents[0]]

    for i in range(1, len(sents)):
        sim = cosine_similarity([embs[i-1]], [embs[i]])[0][0]
        if (sim < threshold and len(cur) >= 2) or len(cur) >= max_sent:
            chunks.append(" ".join(cur))
            cur = [sents[i]]
        else:
            cur.append(sents[i])

    chunks.append(" ".join(cur))
    return chunks

def chunk_text(text, embedder):
    sa = structure_aware_chunk(text)
    return sa if sa else semantic_chunk(text, embedder)
