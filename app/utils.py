from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password,hashed_password):
    verif = pwd_context.verify(plain_password,hashed_password)
    return verif
    print(verif)