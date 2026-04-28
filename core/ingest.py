import uuid
from core.chunking import chunk_text

def ingest_text(text, collection, embedder, batch=64):
    chunks = chunk_text(text, embedder)
    for i in range(0, len(chunks), batch):
        part = chunks[i:i+batch]
        embs = embedder.embed(part)
        collection.add(
            ids=[str(uuid.uuid4()) for _ in part],
            documents=part,
            embeddings=embs
        )
