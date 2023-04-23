from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import databasecon, schemas, models, utils, jwt

router = APIRouter(
    prefix="/authenticate",
    tags=['Authentication']
)


def get_role(user: schemas.RespUserCreated):
    """
    This method maps role from user object to enum value
    """
    if user.role == models.RoleType.admin:
        return "admin"

    elif user.role == models.RoleType.developer:
        return "developer"


def login_user(user_credentials, db):
    """
     JWT stores the login details in a dictionary with keys username and password.
     The details are expected in form-data and not the body!
     We are choosing to verify using the email because it is unique in our application
    """
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not utils.verify(plain_password=user_credentials.password, hashed_password=user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    user_role = get_role(user)

    # Create and Return the token. We can send whatever we want here, we have chosen to send the userid only
    access_token = jwt.create_access_token(data={"user_id": user.id, "role": user_role})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post('/', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(databasecon.get_db)):
    """
    POST API to authenticate and login user
    """
    response = login_user(user_credentials, db)
    return response
