from backend.app.embeddings.embedding_service import EmbeddingService


embedding_service = EmbeddingService()


chunks = [
    "Revenue increased by 18% due to strong demand for data center products.",
    "Operating expenses increased because of higher research and development costs.",
    "The company expects continued growth in artificial intelligence demand.",
    "Revenue declined because of lower demand in the gaming segment.",
]


query = "Why did revenue decline?"


chunk_embeddings = embedding_service.generate_embeddings(chunks)

query_embedding = embedding_service.generate_embedding(query)


results = []


for i, embedding in enumerate(chunk_embeddings):

    similarity = embedding_service.similarity(
        query_embedding,
        embedding
    )

    results.append({
        "chunk": chunks[i],
        "similarity": similarity
    })


results.sort(
    key=lambda x: x["similarity"],
    reverse=True
)


print("Query:")
print(query)

print("\nResults:")

for result in results:

    print(
        f"\nSimilarity: {result['similarity']:.4f}"
    )

    print(
        result["chunk"]
    )