import chromadb
from chromadb.config import Settings
import uuid

CHROMA_DIR = "./chroma_db"

def get_chroma():
    return chromadb.PersistentClient(
        path=CHROMA_DIR,
        settings=Settings(anonymized_telemetry=False)
    )

def get_or_create_collection(client, name):
    try:
        return client.get_collection(name=name)
    except:
        return client.create_collection(name=name)