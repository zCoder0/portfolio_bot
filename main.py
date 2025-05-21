from fastapi import FastAPI , Query
from fastapi.responses import JSONResponse ,FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from src.components.model import user_input
from src.components.preprocessing import load
import os

from fastapi import Request
from pydantic import BaseModel


from src.components.model import user_input
import json


app = FastAPI()
path ='faiss-lib'

class ChatRequest(BaseModel):
    question: str

def remove_puncuation(text:str):
    
    split_words = text.split()
    new_text =""
    for words in split_words:
        
        if words in "*":
            words = "<br>"
        new_text += words + " "
        
    
    return new_text


try:
    if not os.listdir(path):
        pass
except Exception as e:
    print("loading..")
    load()
    

@app.post("/chat")
async def chatWithMe(data: ChatRequest):

    res = user_input(data.question, model_name="gemini-1.5-flash")
    fin_res = remove_puncuation(res['output_text'])
    return {"answer": fin_res}
