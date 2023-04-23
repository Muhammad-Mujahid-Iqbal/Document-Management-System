from typing import List

from fastapi import status, HTTPException, Depends, APIRouter, Response
from ... import models, schemas, jwt
from sqlalchemy.orm import Session
from ...databasecon import get_db


router = APIRouter(
    prefix="/documents/status",
    tags=['Document Status APIs']
)


# API to create a new status for document
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ResDocumentStatus)
def create_document_status(document: schemas.ReqDocumentStatus, db: Session = Depends(get_db),
                current_user: int = Depends(jwt.get_current_user)):
    """
    Enters a new document status object in db
    """
    try:
        # create new document status object and save in db
        new_document_status = models.DocumentStatus(**document.dict())
        db.add(new_document_status)
        db.commit()
        # return newly created document
        return new_document_status

    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=err.args[0])

# API to fetch all documents statuses
@router.get("/", response_model=List[schemas.ResDocumentStatus])
def get_all_documents_status(db: Session = Depends(get_db), current_user: int = Depends(jwt.get_current_user)):
    """
    Returns all documents statuses available in the application
    """
    documents = db.query(models.DocumentStatus).all()
    return documents
