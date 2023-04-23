from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, databasecon, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

jwt_scheme = OAuth2PasswordBearer(tokenUrl='/authenticate/', scheme_name="JWT")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


# data is the access token payload, of type dict
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # A jwt token contains 3 parts: A payload, Secret Key and Algorithem used
    encoded_jwt = jwt.encode(claims=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


# We need to decode the token sent from frontend
# This function simply verifies the token
def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: int = payload.get("user_id")
        role: str = payload.get("role")

        if id is None:
            raise credentials_exception
        if role is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id, role=role)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(jwt_scheme), db: Session = Depends(databasecon.get_db)):
    """
    This is the core method to perform jwt authentication inside APIs.
    It verifies the access token coming in request and after verification, fetch
    the user object from table and return to identify the user
    """
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could Not Validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
