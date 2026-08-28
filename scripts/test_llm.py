from backend.app.llm.llm_service import LLMService


llm_service = LLMService()


question = "Why did revenue decline?"

context = """
Revenue declined because of lower demand in the gaming segment.
"""


answer = llm_service.generate(
    question=question,
    context=context
)


print("Question:")
print(question)

print("\nContext:")
print(context)

print("\nLLM Answer:")
print(answer)