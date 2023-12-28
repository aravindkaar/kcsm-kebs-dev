from fastapi import FastAPI,UploadFile,Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException
from typing import List
from file import FileProcessor,FileBlobWrapper
from json import loads,dumps,dump
import os
from utils import request_open_ai
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "https://example.com",
    "https://example.net",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

@app.get('/')
async def home():
    return 'home'

@app.post('/generator')
async def chat_completion(files:List[UploadFile],project_name:str = Form(),customer_name:str = Form()):
    processed_response = ""
    for index,file in enumerate(files):
        print(file.filename)
        file_uploaded = FileProcessor(file)
        processed_response += f'Content- {index}'+"\n \n"+file_uploaded.process_file_to_txt()+"\n \n"

    response = request_open_ai(processed_response)
    modified_res = response.content
    return {'message':modified_res}
    
@app.get('/upload')
async def chat_completion_v2():
    try:
        root_path = './case_study_generator'
        output_path = './output'
        for folder in os.listdir(root_path):
            processed_response = ""
            for file in os.listdir(root_path+"/"+folder):
                c=0
                file_path = root_path+"/"+folder+"/"+file
                with open(file_path,mode='rb') as ob_file:
                    file_uploaded = FileBlobWrapper(ob_file,filename=file,content_type=file.rsplit('.')[-1])
                    processed_file = FileProcessor(file_uploaded)
                    processed_response += f'Content- {c}'+"\n \n"+processed_file.process_file_to_txt()+"\n \n"
                    c+=1
            modified_res = {}
            try:
                response = request_open_ai(processed_response)
                
                modified_res = {"project":str(folder),'csg':response.content}
            except Exception as e:
                modified_res = {"project":str(folder),'csg':str(e)}

            with open(output_path+"/"+str(folder)+".json",mode='w') as json_file:
                dump(modified_res, json_file)
            
        return "process executed"
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))