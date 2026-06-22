import os
import pandas as pd
import streamlit as st
from src.question_generator import QuestionGenerator
from datetime import datetime

def rerun():
    st.session_state['rerun_trigger'] = not st.session_state.get('rerun_trigger', False)


class QuizeManager:
    def __init__(self):
        self.questions = []
        self.results = []

    def generate_questions(self, generator: QuestionGenerator, topic: str, difficulty: str, question_type: str, num_question: int):
        self.questions = []
        self.results = []

        try:
            for _ in range(num_question):
                if question_type == "Multiple Choice":
                    question = generator.mcq_question_generator(topic, difficulty.lower())
                    self.questions.append({
                        "type": "MCQ",
                        "question": question.question,
                        "options": question.options,
                        "correct_answer": question.correct_answer
                    })
                else:
                    question = generator.Generator_fill_blanks(topic, difficulty)
                    self.questions.append({
                        "type": "Fill in the blanks",
                        "question": question.question,
                        "correct_answer": question.answer
                    })
        except Exception as e:
            st.error(f"Error generating question: {e}")
            return False

        return True
    

    def attempt_quiz(self):
        for i, q in enumerate(self.questions):
            st.markdown(f"**Question {i+1} : {q['question']}**")
            key = f"answer_{i}"  # unique key per widget

            if q['type'] == "MCQ":
                user_ans = st.radio(
                    f"Select an answer for question {i+1}",
                    options=q["options"],
                    key=key
                )
            else:
                user_ans = st.text_input(
                    f"Fill in the blank for question {i+1}",
                    key=key
                )

    def evaluate_quiz(self):
        self.results = []

        for i, q in enumerate(self.questions):
            user_ans = st.session_state.get(f"answer_{i}", "")
            result_dict = {
                "question_number": i+1,
                "question": q['question'],
                "question_type": q["type"],
                "user_answer": user_ans,
                "correct_answer": q["correct_answer"],
                "is_correct": False
            }

            if q["type"] == "MCQ":
                result_dict["options"] = q["options"]
                result_dict['is_correct'] = user_ans == q['correct_answer']
            else:
                result_dict['options'] = []
                result_dict['is_correct'] = user_ans.strip().lower() == q['correct_answer'].strip().lower()

            self.results.append(result_dict)

    def generate_result_dataframe(self):
        if not self.results:
            return pd.DataFrame(columns=["question_number", "question", "user_answer", "correct_answer", "is_correct"])
        return pd.DataFrame(self.results)

    def save_to_csv(self, filename_prefix="quiz_results"):
        if not self.results:
            st.warning("No result to save")
            return None

        df = self.generate_result_dataframe()
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        unique_filename = f"{filename_prefix}_{timestamp}.csv"
        os.makedirs('results', exist_ok=True)
        full_path = os.path.join("results", unique_filename)

        try:
            df.to_csv(full_path, index=False)
            st.success(f"✅ Results saved successfully: {full_path}")
            return full_path
        except Exception as e:
            st.error(f"Failed to save result: {e}")
            return None
