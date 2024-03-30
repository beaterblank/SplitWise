import json
import pyrebase
 
from typing import List, Annotated, Union
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi import APIRouter, Request, Response,Depends, Header

from .utils import authenticate_user

auth_app = APIRouter()

pb = pyrebase.initialize_app(json.load(open('./secrets/firebase_config.json')))
auth = pb.auth()


# signup endpoint
@auth_app.post("/signup")
async def signup(email:str,password:str) -> Response:
    # TODO check if password meets a standard
    if email is None or password is None:
        return HTTPException(detail={
           'message': 'Error! Missing Email or Password'
           }, status_code=400)
    try:
       user = auth.create_user_with_email_and_password(
           email=email,
           password=password
       )
       return JSONResponse(content={
           'message': f'Successfully created user',
           'user': dict(user)["localId"]
           }, status_code=200)    
    except Exception as e:
       print("Error: ", e)
       return HTTPException(detail={
           'message': 'Error Creating User',
           'uid':None}, status_code=400)

# login endpoint
@auth_app.post("/login")
async def login(email:str,password:str)-> Response:
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        jwt = dict(user)['idToken']
        # save this token in user machine
        return JSONResponse(content={'token': jwt}, status_code=200)
    except Exception as e:
        print("Error: ", e)
        return HTTPException(detail={
           'message': 'There was an error logging in'}, status_code=400) 


# request password change endpoint
@auth_app.post("/request_password_change")
async def request_password_change(user:dict = Depends(authenticate_user))-> Response:
    pass

# change password endpoint
@auth_app.post("/change_password")
async def change_password(reset_code:str,password:str)-> Response:
    pass


# TODO verify email
@auth_app.post("/request_verification_email")
async def request_verification_email(user:dict = Depends(authenticate_user))-> Response:
    pass

@auth_app.get("/verify_email")
async def verify_email(code:str)-> Response:
    pass

# ping endpoint
@auth_app.post("/ping")
async def validate(user:dict = Depends(authenticate_user))-> Response:
    return user

# delete user endpoint
@auth_app.post("/delete")
async def delete_user(user:dict = Depends(authenticate_user))-> Response:
    try:
        idToken = user["idToken"]
        output = auth.delete_user_account(idToken)
        return JSONResponse(content=output, status_code=200)
    except Exception as e:
        print("Error: ", e)
        return HTTPException(detail={
           'message': 'There was an error deleting the account'
           }, status_code=400) 


@auth_app.get("/login")
async def render_login():
    # TODO Render login
    pass

@auth_app.get("/change_password")
async def render_change_password(reset_code):
    # TODO UI to enter their new password
    pass
