from backend.app.agents.financial_analyst_agent import (
    FinancialAnalystAgent
)

from backend.app.agents.analyst_orchestrator import (
    AnalystOrchestrator
)

from backend.app.repositories.financial_repository import (
    FinancialRepository
)

from backend.app.embeddings.embedding_service import (
    EmbeddingService
)

from backend.app.vector_db.vector_store import (
    VectorStore
)

from backend.app.retrieval.retrieval_service import (
    RetrievalService
)

from backend.app.rag.rag_service import (
    RAGService
)

from backend.app.llm.llm_service import (
    LLMService
)


# ============================================================
# SERVICES
# ============================================================

repository = FinancialRepository()

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
# EXISTING ANALYST
# ============================================================

financial_analyst = FinancialAnalystAgent(
    repository=repository,
    rag_service=rag_service
)


# ============================================================
# ORCHESTRATOR
# ============================================================

orchestrator = AnalystOrchestrator(
    financial_analyst=financial_analyst
)


# ============================================================
# TEST
# ============================================================

questions = [
    "What was the company's revenue?",
    "What is the company's ROA?",
    "Why did revenue decline?"
]


for question in questions:

    result = orchestrator.analyze(
        question=question,
        company_id=1,
        fiscal_year=2025
    )

    print("\n" + "=" * 60)

    print("Question:")
    print(question)

    print("\nRoute:")
    print(result["route"])

    print("\nAnswer:")
    print(result["answer"])