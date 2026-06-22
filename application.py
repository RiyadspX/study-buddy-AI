import os
import streamlit as st
from dotenv import load_dotenv
from src.helpers import *
from src.question_generator import QuestionGenerator
load_dotenv()

class Main:
    st.set_page_config(page_title="Study Buddy AI")

    if "quiz_manager" not in st.session_state:
        st.session_state.quiz_manager=QuizeManager()

    if "quiz_generated" not in st.session_state:
        st.session_state.quiz_generated=False

    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted=False

    if 'rerun_trigger'not in st.session_state:
        st.session_state.rerun_trigger = False
    
    st.title("Study Buddy AI New NEW NEW NEW")
    
    st.sidebar.header("Quiz Settings")

    question_type=st.sidebar.selectbox("Select Question Type", ["Multiple Choice", "Fill in the blanks"], index=0)

    topic=st.sidebar.text_input("Enter Topic",placeholder="Indian History, Geography")

    difficulty=st.sidebar.selectbox("Diffiiculty Level", ["Easy","Medium","Hard"],index=1)

    num_questions=st.sidebar.number_input("Number of Questions",min_value=1,max_value=10,value=5)

    if st.sidebar.button("Generate Quiz"):
        st.session_state.quiz_submitted=False

        generator=QuestionGenerator()
        st.session_state.quiz_manager.generate_questions(generator,topic,difficulty,question_type,num_questions)
        st.session_state.quiz_generated=True
        rerun()
    if st.session_state.quiz_generated and st.session_state.quiz_manager.questions:
        st.header("Quiz")
        st.session_state.quiz_manager.attempt_quiz()
        if st.button("Submit Quiz"):
            st.session_state.quiz_manager.evaluate_quiz()
            st.session_state.quiz_submitted=True
            rerun()

            if st.session_state.quiz_submitted:
                st.header("Quiz Results:")
                result_df = st.session_state.quiz_manager.generate_result_dataframe()

                if not result_df.empty:
                    correct_count = result_df["is_correct"].sum()
                    total_questions = len(result_df)
                    score_percentage = (correct_count / total_questions) * 100
                    st.write(f"Score: {score_percentage:.2f}%")

                    for _, result in result_df.iterrows():
                        question_number = result['question_number']
                        if result['is_correct']:
                            st.success(f"✅ Question {question_number} : {result['question']}")
                        else:
                            st.error(f"❌ Question {question_number} : {result['question']}")
                            st.write(f"Your answer : {result['user_answer']}")
                            st.write(f"Correct answer : {result['correct_answer']}")
                        st.markdown("-----")

                    # Save results
                    if st.button("Save Result"):
                        saved_file = st.session_state.quiz_manager.save_to_csv()
                        if saved_file:
                            st.session_state["saved_file"] = saved_file  # store in session state
                            st.success("✅ Results saved successfully!")

                    # Always show download if file exists in session_state
                    if "saved_file" in st.session_state:
                        with open(st.session_state["saved_file"], "rb") as f:
                            st.download_button(
                                label="Download Results",
                                data=f.read(),
                                file_name=os.path.basename(st.session_state["saved_file"]),
                                mime="text/csv"
                            )
                else:
                    st.warning("⚠️ No results available")


if __name__=="__main__":
    Main()




    