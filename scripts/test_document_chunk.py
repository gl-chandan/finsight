from backend.app.embeddings.document_chunk import DocumentChunk


chunk = DocumentChunk(
    text="Revenue increased by 18% due to strong demand.",
    document_name="NVIDIA_Annual_Report_2025.pdf",
    page_number=47
)


print("Document:", chunk.document_name)
print("Page:", chunk.page_number)
print("Text:", chunk.text)