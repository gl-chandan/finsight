from backend.app.embeddings.document_chunk import DocumentChunk
from backend.app.embeddings.embedding_service import EmbeddingService


embedding_service = EmbeddingService()


chunks = [
    DocumentChunk(
        text="Revenue increased by 18% due to strong demand for data center products.",
        document_name="NVIDIA_Annual_Report_2025.pdf",
        page_number=47
    ),

    DocumentChunk(
        text="Operating expenses increased because of higher research and development costs.",
        document_name="NVIDIA_Annual_Report_2025.pdf",
        page_number=48
    ),

    DocumentChunk(
        text="Revenue declined because of lower demand in the gaming segment.",
        document_name="NVIDIA_Annual_Report_2025.pdf",
        page_number=49
    )
]


texts = [chunk.text for chunk in chunks]

embeddings = embedding_service.generate_embeddings(texts)


for chunk, embedding in zip(chunks, embeddings):

    print("\nDocument:", chunk.document_name)
    print("Page:", chunk.page_number)
    print("Text:", chunk.text)
    print("Embedding dimensions:", len(embedding))
    print("First 5 values:", embedding[:5])