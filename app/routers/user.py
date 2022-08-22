from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from app.database import get_db
from sqlalchemy.orm import Session

from app import models, oauth2, schemas, utils

router = APIRouter(
    prefix="/users",
    tags=["Users"] # this is to group them on the documentation
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hash the password - user.password
    user.password = utils.hash(user.password)

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} does not exist")

    return user
