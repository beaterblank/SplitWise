import os
import uvicorn

from fastapi import FastAPI,APIRouter
from fastapi.middleware.cors import CORSMiddleware

from auth.auth import auth_app

app = FastAPI(
    title="WiseSplit",
    description="App to handle basic day to day finances in a group"
)   

allow_all = ['*']
app.add_middleware(
   CORSMiddleware,
   allow_origins=allow_all,
   allow_credentials=True,
   allow_methods=allow_all,
   allow_headers=allow_all
)

api_router = APIRouter()
api_router.include_router(auth_app,prefix="/auth",tags=['users'])

app.include_router(router = api_router,prefix="/v1")

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 8000))
    WORKERS = int(os.environ.get("WORKERS", 1))
    uvicorn.run(
        "wise_split:app", 
        host="0.0.0.0", 
        port=PORT, 
        workers=WORKERS, 
        reload=True
    )
