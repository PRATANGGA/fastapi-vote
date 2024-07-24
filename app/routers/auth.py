from fastapi import APIRouter, Depends, Response ,status,HTTPException, responses
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from .. import database,schemas,models,utils,oauth2

router = APIRouter(tags=["Authentication"])

@router.post("/login",response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")
    
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")
    
    # create token
    # return token
    print(user.id)
    print(type(user.id))
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    print(type(access_token))
    return {"access_token" : access_token, "token_type" : "bearer"} 