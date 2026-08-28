import chromadb


class VectorStore:

    def __init__(
        self,
        collection_name: str = "financial_documents"
    ):
        self.client = chromadb.PersistentClient(
            path="./chroma_db"
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

    def add(
        self,
        document_id: str,
        text: str,
        embedding: list[float],
        metadata: dict
    ):
        self.collection.add(
            ids=[document_id],
            documents=[text],
            embeddings=[embedding],
            metadatas=[metadata]
        )

    def count(self) -> int:

        return self.collection.count()
    def search(
    self,
    query_embedding: list[float],
    n_results: int = 3
):

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

        formatted_results = []

        for i, document in enumerate(
            results["documents"][0]
        ):

            formatted_results.append({
                "text": document,
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i]
            })

        return formatted_results