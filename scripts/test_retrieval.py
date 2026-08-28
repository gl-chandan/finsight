from backend.app.embeddings.embedding_service import EmbeddingService
from backend.app.vector_db.vector_store import VectorStore
from backend.app.retrieval.retrieval_service import RetrievalService


embedding_service = EmbeddingService()

vector_store = VectorStore()

retrieval_service = RetrievalService(
    embedding_service=embedding_service,
    vector_store=vector_store
)


query = "Why did revenue decline?"


results = retrieval_service.retrieve(
    query=query,
    n_results=3
)


print("Query:")
print(query)

print("\nRetrieved chunks:")


for i, result in enumerate(results):

    print(f"\nResult {i + 1}")

    print("Text:")
    print(result["text"])

    print("Metadata:")
    print(result["metadata"])

    print("Distance:")
    print(result["distance"])