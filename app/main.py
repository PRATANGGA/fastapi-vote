from fastapi import FastAPI, Depends
from . import models
from .database import engine
from .routers import post,user,auth,vote
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated



# models.Base.metadata.create_all(bind=engine)
app = FastAPI()
# Dependency
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
        
@app.get("/")
async def read_root():
    return {"Hello": "My APIs server is running"}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
# @app.get("/sqlalchemy")
# def test_post(db: Session = Depends(get_db)):
#     return {"data": "Testing SQLAlchemy"}


      

