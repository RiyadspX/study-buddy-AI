from dotenv import load_dotenv
import os

load_dotenv()

class Settings:

    GROQ_API_KEY=os.getenv("GROQ_API_KEY")
    model_name= "groq/compound"
    temperature=0.7
    max_retries=2

settings=Settings()