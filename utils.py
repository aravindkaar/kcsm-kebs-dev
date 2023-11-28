from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
from dotenv import load_dotenv
import os
load_dotenv()

def request_claude(extracted_text):

    anthropic = Anthropic(
        api_key=os.getenv('API_KEY'),
    )

    system_prompt = f"""
                You are a highly skilled AI trained in language comprehension and question and answering.
                I would like you to read the following contents which are numbered in which each content 
                is a parsed document content.Read all the contents carefully and thoroughly and answer the follwing questions
                keenly. the answer's can be found in each content and mainly dont hallucinate or assume.
                Generate the answers in json format where key is the question number.
                
                Questions:
                1) What is industry vertical relating to the context?
                2) Customer Overview with name,location,business scope and company size?
                3) Project Overview with Objective, Techstack,Key benefits?
                4) What is the implementation approach explain the steps?
                5) Explain challenges involved and solutions?
                6) Brief results and impact?
                7) What are the project deliverables (if any) in each phase and their status?

            {extracted_text}  
            """
    completion = anthropic.completions.create(
        model="claude-2",
        max_tokens_to_sample=11300,
        prompt=system_prompt,
    )

    return completion.completion