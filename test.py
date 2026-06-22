from src.groq_client import get_qroq_llm

llm = get_qroq_llm()

response = llm.invoke("Say hello in one sentence")

print(response)
print("----")
print(response.content)