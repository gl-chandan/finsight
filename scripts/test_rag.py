from backend.app.embeddings.embedding_service import EmbeddingService
from backend.app.vector_db.vector_store import VectorStore
from backend.app.retrieval.retrieval_service import RetrievalService
from backend.app.rag.rag_service import RAGService
from backend.app.llm.llm_service import LLMService
from dotenv import load_dotenv

load_dotenv()

# ============================================================
# CREATE SERVICES
# ============================================================

embedding_service = EmbeddingService()

vector_store = VectorStore()

retrieval_service = RetrievalService(
    embedding_service=embedding_service,
    vector_store=vector_store
)

llm_service = LLMService()

rag_service = RAGService(
    retrieval_service=retrieval_service,
    llm_service=llm_service
)


# ============================================================
# TEST QUESTIONS
# ============================================================

questions = [
    "Why did revenue decline?",
    "Why did operating expenses increase?",
    "What risks did management mention?",
    "What was NVIDIA's employee headcount?",
    "What is driving future growth?"
]


# ============================================================
# RUN TESTS
# ============================================================

for question in questions:

    result = rag_service.answer(
        question=question,
        n_results=3
    )

    print("\n" + "=" * 60)

    print("\nQuestion:")
    print(question)

    print("\nAnswer:")
    print(result["answer"])

    print("\nSources:")

    if not result.get("sources"):
        print("No sources found.")

    else:

        for source in result["sources"]:

            print(
                f"Document: {source['document']}"
            )

            print(
                f"Page: {source['page']}"
            )

            print(
                f"Text: {source['text']}"
            )

            print()