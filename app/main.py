import os
import json
import logging
import uvicorn
import pyrebase
import firebase_admin
 
from typing import List, Annotated
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from firebase_admin import credentials, auth
from fastapi.middleware.cors import CORSMiddleware


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

app = FastAPI()
allow_all = ['*']
app.add_middleware(
   CORSMiddleware,
   allow_origins=allow_all,
   allow_credentials=True,
   allow_methods=allow_all,
   allow_headers=allow_all
)


cred = credentials.Certificate('./splitwise_service_account_keys.json')
firebase = firebase_admin.initialize_app(cred)
pb = pyrebase.initialize_app(json.load(open('firebase_config.json')))

# signup endpoint
@app.post("/signup", include_in_schema=False)
async def signup(request: Request):
   req = await request.json()
   email = req['email']
   password = req['password']
   # TODO check if password meets a standard
   if email is None or password is None:
       return HTTPException(detail={'message': 'Error! Missing Email or Password'}, status_code=400)
   try:
       user = auth.create_user(
           email=email,
           password=password
       )
       return JSONResponse(content={'message': f'Successfully created user {user.uid}','uid':user.uid}, status_code=200)    
   except:
       return HTTPException(detail={'message': 'Error Creating User','uid':None}, status_code=400)

# login endpoint
@app.post("/login", include_in_schema=False)
async def login(request: Request):
   req_json = await request.json()
   email = req_json['email']
   password = req_json['password']
   try:
       user = pb.auth().sign_in_with_email_and_password(email, password)
       jwt = user['idToken']
       # save this token in user machine
       return JSONResponse(content={'token': jwt}, status_code=200)
   except:
       return HTTPException(detail={'message': 'There was an error logging in'}, status_code=400) 


# ping endpoint
@app.post("/ping", include_in_schema=False)
async def validate(request: Request):
   # TODO use a middleware for this
   headers = request.headers
   jwt = headers.get('authorization')
   logger.info(f"jwt:{jwt}")
   user = auth.verify_id_token(jwt)
   return user["uid"]

@app.get("/")
def home():
    return {"message":"Hello World"}




if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 8000))
    WORKERS = int(os.environ.get("WORKERS", 1))
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, workers=WORKERS)
