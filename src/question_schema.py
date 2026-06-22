from typing import List
from pydantic import BaseModel,Field,field_validator

class MCQQuestion(BaseModel):
    question : str = Field(description="The question text")
    options : list[str] = Field(description="List of 4 options")
    correct_answer : str =Field(description="The correct answer from the options")

    @field_validator('question',check_fields=True)
    def clean_question(cls,v):
        if isinstance(v,dict):
           return v.get("description",str(v))
        return str(v)
    
class FillInTheBlanks(BaseModel):
    question: str = Field(description="The question text")
    answer: str = Field(description="The answer text")
     
    @field_validator('question', check_fields=True)
    def clean_question(cls, v):
        if isinstance(v, dict):
            return v.get("description", str(v))
        return str(v)

    @field_validator('answer', check_fields=True)
    def clean_answer(cls, v):
        if isinstance(v, dict):
            return v.get("description", str(v))
        return str(v)

