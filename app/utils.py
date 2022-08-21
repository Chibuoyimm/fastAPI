from passlib.context import CryptContext # for password hashing or hiding


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # this is just telling passlib that we want to use the bcrypt algorithm for hashing

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)