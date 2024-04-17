import os
import json
import pandas as pd
from src.mcqgenerator.logger import logging
from src.mcqgenerator.utils import get_table_data, read_file
from langchain import HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain


os.environ['HUGGINGFACEHUB_API_TOKEN'] = "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"


llm = HuggingFaceHub(repo_id='google/flan-t5-large', model_kwargs={'temperature':0})


template = """
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz of {number} multiple choice questions for {subject} students in {tone} tone.
Make sure the question are not repeated and check all the questions to be conforming the text as well.
Make sure ti format your response like RESPONSE_JSON below and use it as a guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}

"""

quiz_generation_prompt = PromptTemplate(input_variables=["text", "number", "subject", "tone", "response_json"], template=template)


quiz_chain = LLMChain(llm=llm, prompt=quiz_generation_prompt, output_key="quiz", verbose=True)


template2 = """
You are an expert english gramarien and write. Given a Mutiple Choice Quiz for {subject} students. \
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis.
if the quiz is not at per with the cognitive and analytical abilities of the students, \
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities.
QUIZ_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""


quiz_evaluation_prompt = PromptTemplate(input_variables=["subject", "quiz"], template=template2)


review_chain = LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key="review", verbose=True)


generative_evaluate_chain = SequentialChain(chains=[quiz_chain, review_chain],
                                            input_variables=["text", "number", "subject", "tone", "response_json"],
                                            output_variables=["quiz", "review"], verbose=True,)

print(generative_evaluate_chain)
