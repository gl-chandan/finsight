from sentence_transformers import SentenceTransformer
import numpy as np


class EmbeddingService:

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2"
    ):
        self.model = SentenceTransformer(model_name)

    def generate_embedding(
        self,
        text: str
    ) -> list[float]:

        embedding = self.model.encode(text)

        return embedding.tolist()

    def generate_embeddings(
        self,
        texts: list[str]
    ) -> list[list[float]]:

        embeddings = self.model.encode(texts)

        return embeddings.tolist()

    def similarity(
        self,
        embedding_a: list[float],
        embedding_b: list[float]
    ) -> float:

        a = np.array(embedding_a)
        b = np.array(embedding_b)

        return float(
            np.dot(a, b) / (
                np.linalg.norm(a) *
                np.linalg.norm(b)
            )
        )