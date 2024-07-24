from fastapi import FastAPI, Response ,status,HTTPException,Depends, APIRouter
from .. import models,schemas,utils
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(tags=["Users"])

@router.post("/users",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
async def create_user(user: schemas.UserBase,db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO users(email,password) VALUES(%s,%s) RETURNING * """,(user.email,user.password))
    print(user)
    print(user.dict())
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/users/{id}",response_model=schemas.UserOut)
def get_user(id: int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id: {id} does not exist")
    return user