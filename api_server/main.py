from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi import HTTPException
from  manager import ModelTemplate
import os

model = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    model_path = os.getenv("MODEL_PATH")
    model = ModelTemplate(model_path=model_path)
    yield

app = FastAPI(lifespan=lifespan)


from fastapi import FastAPI, HTTPException, Request

@app.post("/model/generate")
async def process_data(request: Request):
    try:
        request_data = await request.json()

        prompt = request_data.get("prompt")
        if not prompt:
            raise HTTPException(status_code=400, detail="Missing 'prompt' in request")
        
        result = model.generate_prompt(prompt) 
        return result 

    except KeyError: 
        raise HTTPException(status_code=400, detail="Invalid request format")
    except Exception as e: 
        raise HTTPException(status_code=500, detail=str(e)) 
