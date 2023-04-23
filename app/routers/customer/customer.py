from fastapi import status, HTTPException, Depends, APIRouter
from ... import models, schemas, jwt
from sqlalchemy.orm import Session
from ...databasecon import get_db
from typing import List

router = APIRouter(
    prefix="/customers",
    tags=['Customers APIs']
)


# API to create a new Customer into the system
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ResCustomer)
def create_customer(customer: schemas.ReqCustomer, db: Session = Depends(get_db),
                    current_user: int = Depends(jwt.get_current_user)):
    """
    Creates a new Customer in the application
    """
    try:
        # create new Customer type model object and save in db
        new_customer = models.Customer(**customer.dict())
        db.add(new_customer)
        db.commit()
        # return newly created object
        return new_customer

    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=err.args[0])


# API to fetch all customers
@router.get("/", response_model=List[schemas.ResCustomer])
def get_all_customers(db: Session = Depends(get_db), current_user: int = Depends(jwt.get_current_user)):
    """
    Returns all customers available in the application
    """
    customers = db.query(models.Customer).all()
    return customers
