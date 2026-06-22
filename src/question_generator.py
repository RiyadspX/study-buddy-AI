from langchain_core.output_parsers import PydanticOutputParser
from src.utils.logger import get_logger
from src.utils.costom_exception import CostomException
from src.config import settings
from src.groq_client import get_qroq_llm
from src.prompt_template import mcq_prompt_template,fill_blank_prompt_template
from src.question_schema import MCQQuestion,FillInTheBlanks

class QuestionGenerator:
    def __init__(self):
        self.llm=get_qroq_llm()
        self.logger=get_logger(self.__class__.__name__)

    def _retry_and_parse(self, topic, difficulty, parser, prompt_template):
        try:
            response = self.llm.invoke(prompt_template.format(topic=topic, difficulty=difficulty))
            print(f"[DEBUG] Raw LLM response: {response}")  # 👈 Add this
            question = parser.parse(response.content)

            return question
        except Exception as e:
            import traceback
            print(f"[ERROR] Failed to parse FillInTheBlank question: {e}")
            traceback.print_exc()
            raise CostomException("FillInTheBlank question Generation Failed", e)


    def mcq_question_generator(self,topic:str,difficulty:str='medium') -> MCQQuestion:
        try:
            parser=PydanticOutputParser(pydantic_object=MCQQuestion)
            question= self._retry_and_parse(topic, difficulty, parser, mcq_prompt_template)
            if len(question.options)!=4 or question.correct_answer not in question.options:
                raise ValueError("Invalid MCQ structure")
            self.logger.info("Generated a valid MCQ Question")
            return question
        except Exception as e:
               self.logger.error(f"error coming : {str(e)}")
               raise ValueError("MCQ Generation Failed",e)
    
    def Generator_fill_blanks(self,topic:str,difficulty:str='medium') -> FillInTheBlanks:
        try:
            parser=PydanticOutputParser(pydantic_object=FillInTheBlanks)
            question= self._retry_and_parse(topic, difficulty, parser, fill_blank_prompt_template)
            if  "___" not in question.question:
                raise ValueError("Fill in blanks should contain '___'")
            self.logger.info("Generated a valid Fill in Blanks Question")
            return question
        except Exception as e:
               self.logger.error(f"error coming : {str(e)}")
               raise CostomException("FillInTheBlank question Generation Failed",e)
        
            