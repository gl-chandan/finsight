
from backend.app.agents.financial_analyst_agent import (
    FinancialAnalystAgent
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
# CREATE SERVICES
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
# CREATE FINANCIAL ANALYST AGENT
# ============================================================

agent = FinancialAnalystAgent(
    repository=repository,
    rag_service=rag_service
)


# ============================================================
# TEST QUESTIONS
# ============================================================

'''questions = [

    # --------------------------------------------------------
    # BASIC FINANCIAL METRICS
    # --------------------------------------------------------

    "What was the company's revenue?",

    "What was the company's net income?",

    "What is the company's ROA?",

    "What is the company's ROE?",

    "What is the company's net margin?",


    # --------------------------------------------------------
    # SIMPLE COMPARISONS
    # --------------------------------------------------------

    "How much did revenue grow?",

    "Did net income increase?",

    "Compare revenue between 2024 and 2025.",

    "Compare net income between 2024 and 2025.",

    "Is the company's debt position improving?",


    # --------------------------------------------------------
    # DOCUMENT / RAG QUESTIONS
    # --------------------------------------------------------

    "Why did revenue decline?",

    "Why did operating expenses increase?",

    "What risks did management mention?",

    "What was NVIDIA's employee headcount?",
    "What is the company's stock price?",
    "What is the company's CEO?"
]'''
questions = [

    # 1. Basic metric
    "What was the company's revenue?",

    # 2. Calculated metric
    "What is the company's ROA?",

    # 3. Comparison
    "Compare revenue between 2024 and 2025.",

    # 4. RAG
    "Why did revenue decline?",

    # 5. Unsupported
    "What is the company's stock price?"

]


# ============================================================
# RUN TESTS
# ============================================================

for question in questions:

    print("\n" + "=" * 60)

    print("Question:")
    print(question)

    try:

        result = agent.analyze(
            question=question,
            company_id=1,
            fiscal_year=2025
        )

        print("\nRoute:")
        print(result.get("route"))

        print("\nAnswer:")
        print(result.get("answer"))


        # ----------------------------------------------------
        # RAG SOURCES
        # ----------------------------------------------------

        sources = result.get("sources", [])

        if sources:

            print("\nSources:")

            for source in sources:

                print(
                    f"Document: "
                    f"{source.get('document', 'N/A')}"
                )

                print(
                    f"Page: "
                    f"{source.get('page', 'N/A')}"
                )

                print(
                    f"Text: "
                    f"{source.get('text', 'N/A')}"
                )

    except Exception as error:

        print("\nERROR:")
        print(error)