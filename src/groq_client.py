from langchain_groq import ChatGroq
from src.config import settings

def get_qroq_llm():
    return ChatGroq(api_key=settings.GROQ_API_KEY,
                    model=settings.model_name,
                    temperature=settings.temperature)
