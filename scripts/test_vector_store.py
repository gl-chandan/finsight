from backend.app.embeddings.embedding_service import EmbeddingService
from backend.app.vector_db.vector_store import VectorStore


embedding_service = EmbeddingService()

vector_store = VectorStore()


query = "Why did revenue decline?"


query_embedding = embedding_service.generate_embedding(
    query
)


results = vector_store.search(
    query_embedding=query_embedding,
    n_results=3
)


print("Query:")
print(query)

print("\nTop relevant chunks:")


for i, result in enumerate(results):

    print(f"\nResult {i + 1}")

    print("Text:")
    print(result["text"])

    print(
        "Metadata:",
        result["metadata"]
    )

    print(
        "Distance:",
        result["distance"]
    )