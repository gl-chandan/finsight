from backend.app.embeddings.embedding_service import EmbeddingService
from backend.app.vector_db.vector_store import VectorStore


class RetrievalService:

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: VectorStore
    ):
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def retrieve(
    self,
    query: str,
    n_results: int = 3,
    max_distance: float = 1.0
):

        query_embedding = self.embedding_service.generate_embedding(
            query
        )

        results = self.vector_store.search(
            query_embedding,
            n_results=n_results
        )

        filtered_results = []

        for result in results:

            distance = result.get("distance")

            if distance is None:
                continue

            if distance <= max_distance:

                filtered_results.append(result)

        return filtered_results