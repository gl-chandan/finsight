
from fastapi import APIRouter, Depends

from backend.app.agents.financial_analyst_agent import (
    FinancialAnalystAgent
)

from backend.app.agents.analyst_orchestrator import (
    AnalystOrchestrator
)

from backend.app.repositories.financial_repository import (
    FinancialRepository
)

from backend.app.schemas.analyst import (
    AnalystQueryRequest,
    AnalystQueryResponse
)

from backend.app.core.dependencies import (
    get_financial_repository
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


router = APIRouter(
    prefix="/api/analyst",
    tags=["Financial Analyst"]
)


def get_financial_analyst_agent(
    repository: FinancialRepository = Depends(
        get_financial_repository
    )
):

    # ----------------------------------------------------------
    # Embedding service
    # ----------------------------------------------------------

    embedding_service = EmbeddingService()

    # ----------------------------------------------------------
    # Vector store
    # ----------------------------------------------------------

    vector_store = VectorStore()

    # ----------------------------------------------------------
    # Retrieval service
    # ----------------------------------------------------------

    retrieval_service = RetrievalService(
        embedding_service=embedding_service,
        vector_store=vector_store
    )

    # ----------------------------------------------------------
    # LLM service
    # ----------------------------------------------------------

    llm_service = LLMService()

    # ----------------------------------------------------------
    # RAG service
    # ----------------------------------------------------------

    rag_service = RAGService(
        retrieval_service=retrieval_service,
        llm_service=llm_service
    )

    # ----------------------------------------------------------
    # Financial Analyst Agent
    # ----------------------------------------------------------

    financial_analyst = FinancialAnalystAgent(
        repository=repository,
        rag_service=rag_service
    )

    # ----------------------------------------------------------
    # Analyst Orchestrator
    # ----------------------------------------------------------

    return AnalystOrchestrator(
        financial_analyst=financial_analyst
    )


@router.post(
    "/query",
    response_model=AnalystQueryResponse
)
def analyst_query(
    request: AnalystQueryRequest,
    agent: AnalystOrchestrator = Depends(
        get_financial_analyst_agent
    )
):

    result = agent.analyze(
        question=request.question,
        company_id=request.company_id,
        fiscal_year=request.fiscal_year
    )

    return result
