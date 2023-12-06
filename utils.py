from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
from dotenv import load_dotenv
import os
load_dotenv()

def request_claude(extracted_text):

    anthropic = Anthropic(
        api_key=os.getenv('API_KEY'),
    )

    system_prompt = f"""
                You are a highly skilled AI trained in generating case study document and question and answering.
                Read all the contents carefully,keenly and thoroughly and answer the follwing questions in json format
                wherein each key is question number and the value is the corresponding answer if there is subheading inturn use it as a key.
                The answer's can be found in each content,include all relevant details and mainly dont hallucinate or assume.
                
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
        temperature=0,
        prompt=f"{HUMAN_PROMPT}{system_prompt}{AI_PROMPT}"
    )

    return completion.completion.split(':',1)[-1]