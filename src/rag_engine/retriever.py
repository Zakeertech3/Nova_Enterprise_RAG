import os
from qdrant_client import QdrantClient
from qdrant_client.http import models as rest
from langchain_qdrant import QdrantVectorStore
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings

QDRANT_PATH = os.path.join("data", "qdrant_db")
COLLECTION_NAME = "nova_assist_docs"

def get_retriever(user_role: str, source_type: str = "all"):
    embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    client = QdrantClient(path=QDRANT_PATH)
    vector_store = QdrantVectorStore(
        client=client, collection_name=COLLECTION_NAME, embedding=embeddings,
    )

    must_conditions = [
        rest.FieldCondition(
            key="metadata.allowed_roles", match=rest.MatchAny(any=[user_role]),
        )
    ]
    
    if source_type != "all":
        must_conditions.append(
            rest.FieldCondition(
                key="metadata.source_type", match=rest.MatchValue(value=source_type),
            )
        )

    rbac_filter = rest.Filter(must=must_conditions)
    
    return vector_store.as_retriever(
        search_type="similarity", search_kwargs={"k": 4, "filter": rbac_filter}
    )