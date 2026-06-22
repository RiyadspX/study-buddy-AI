from langchain_core.prompts import PromptTemplate

mcq_prompt_template = PromptTemplate(
    template=(
        "Generate one {difficulty} multiple-choice question about {topic}.\n\n"
        "Return ONLY a valid JSON object (no extra text, no markdown) with exactly these fields:\n"
        "- 'question': A clear, specific question (string)\n"
        "- 'options': An array of exactly 4 strings\n"
        "- 'correct_answer': One of the options that is the correct answer (string)\n\n"
        "Example:\n"
        '{{\n'
        '  "question": "What is the capital of France?",\n'
        '  "options": ["London", "Berlin", "Paris", "Madrid"],\n'
        '  "correct_answer": "Paris"\n'
        '}}\n\n'
        "Your response must be ONLY the JSON object:"
    ),
    input_variables=["topic", "difficulty"]
)


fill_blank_prompt_template = PromptTemplate(
    template=(
        "Generate one {difficulty} fill-in-the-blank style question about {topic}.\n\n"
        "The question MUST contain exactly one blank represented as '___'.\n\n"
        "Return ONLY a valid JSON object (no extra text, no markdown) with exactly these fields:\n"
        "- 'question': A sentence with '___' marking the blank (string)\n"
        "- 'answer': The correct word or phrase that belongs in the blank (string)\n\n"
        "Example:\n"
        '{{\n'
        '  "question": "The capital of France is ___.",\n'
        '  "answer": "Paris"\n'
        '}}\n\n'
        "Your response must be ONLY the JSON object:"
    ),
    input_variables=["topic", "difficulty"]
)
