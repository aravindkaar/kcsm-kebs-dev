from fastapi import FastAPI,UploadFile,Form
from fastapi.middleware.cors import CORSMiddleware
from file import FileProcessor
from json import loads,dumps
from utils import request_claude
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

@app.route('/')
async def home():
    return 'home'

@app.post('/generator')
async def chat_completion(files:list[UploadFile],project_name:str = Form(),customer_name:str = Form()):
    processed_response = ""
    for index,file in enumerate(files):
        print(file.filename)
        file_uploaded = FileProcessor(file)
        processed_response += f'Content- {index}'+"\n \n"+file_uploaded.process_file_to_txt()+"\n \n"

    response = request_claude(processed_response)
    modified_res = loads(response)
    print(modified_res)
    return {'mess':modified_res}
    