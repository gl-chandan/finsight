from backend.app.retrieval.retrieval_service import RetrievalService
from backend.app.llm.llm_service import LLMService


class RAGService:

    def __init__(
        self,
        retrieval_service: RetrievalService,
        llm_service: LLMService
    ):
        self.retrieval_service = retrieval_service
        self.llm_service = llm_service

    def answer(
        self,
        question: str,
        n_results: int = 3
    ):

        # 1. Retrieve relevant chunks
        results = self.retrieval_service.retrieve(
            query=question,
            n_results=n_results
        )

        if not results:

            return {
                "answer": "I couldn't find enough information in the uploaded documents.",
                "sources": []
            }

        # 2. Build context
        context_parts = []

        for result in results:

            text = result["text"]

            metadata = result["metadata"]

            document_name = metadata.get(
                "document_name",
                "Unknown document"
            )

            page_number = metadata.get(
                "page_number",
                "Unknown page"
            )

            context_parts.append(
                f"Source: {document_name}, "
                f"Page: {page_number}\n"
                f"{text}"
            )

        context = "\n\n".join(
            context_parts
        )

        # 3. Send question + context to LLM
        answer = self.llm_service.generate(
            question=question,
            context=context
        )

        sources = []

        for result in results:

            metadata = result["metadata"]

            sources.append({
            "document": metadata.get(
                "document_name",
                "Unknown document"
            ),
            "page": metadata.get(
                "page_number",
                "Unknown page"
            ),
            "text": result["text"]
        })


        return {
            "answer": answer,
            "sources": sources
        }