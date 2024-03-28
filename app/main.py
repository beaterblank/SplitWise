import os
import logging
import uvicorn

from fastapi import FastAPI
from typing import List, Annotated
from fastapi.responses import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

app = FastAPI()

@app.get("/home")
def home():
    return {"message":"Hello World"}

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 8000))
    WORKERS = int(os.environ.get("WORKERS", 1))
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, workers=WORKERS)
