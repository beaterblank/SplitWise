import jwt

from .models import AuthItem

def authenticate_user(auth_item: AuthItem):
    idToken = auth_item.auth_token
    data = jwt.decode(idToken.encode(), 
            options={"verify_signature": False})
    try:
        user = auth.get_account_info(idToken)
    except Exception as e:
        print("Error: ", e)
        return HTTPException(detail={
           'message': 'There was an error authenticating'
           }, status_code=400)
    data = dict(**data,**dict(user))
    return data
