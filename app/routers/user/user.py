from fastapi import status, HTTPException, Depends, APIRouter, Response
from ... import models, schemas, utils
from sqlalchemy.orm import Session
from ...databasecon import get_db
from typing import Optional, List

router = APIRouter(
    prefix="/users",
    tags=['User APIs']
)


# API to register a new User
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.RespUserCreated)
def create_user(user: schemas.ReqUserCreate, db: Session = Depends(get_db)):
    """
    Creates a new user in the application
    """
    try:
        # Hash the password coming in request
        hashed_password = utils.pwdhasher(user.password)
        # assign hashed password to user
        user.password = hashed_password
        # save user object in db
        new_user = models.User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        # return user
        return new_user

    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=err.args[0])


# API to show all registered users
@router.get("/", response_model=List[schemas.RespUserCreated])
def get_all_users(db: Session = Depends(get_db), search: Optional[str] = ""):
    """
    Returns all users saved in db for this application. It also searches users based on given email
    """
    users = db.query(models.User).filter(
        models.User.email.contains(search)).all()
    return users


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_a_user(id: int, db: Session = Depends(get_db) ):
    """
    Deletes the user for given Id
    """
    user_query = db.query(models.User).filter(
        models.User.id == id)
    user = user_query.first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with the id: {id} was not found")

    user_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
