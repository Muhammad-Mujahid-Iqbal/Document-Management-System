from typing import List

from fastapi import status, HTTPException, Depends, APIRouter
from ... import models, schemas, jwt
from sqlalchemy.orm import Session
from ...databasecon import get_db


router = APIRouter(
    prefix="/documents/metadata",
    tags=['Document Metadata APIs']
)


# API to create a new metadata document
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ResDocumentMetadata)
def create_document_metadata(document: schemas.ReqDocumentMetadata, db: Session = Depends(get_db),
                current_user: int = Depends(jwt.get_current_user)):
    """
    Saves a new document metadata in DB
    """
    try:
        # create new metadata object and save in db
        new_document_metadata = models.DocumentMetadata(**document.dict())
        new_document_metadata.uploadedByUserId=current_user.id
        db.add(new_document_metadata)
        db.commit()
        #  return newly created object
        return new_document_metadata

    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=err.args[0])


# API to fetch all documents metadata
@router.get("/", response_model=List[schemas.ResDocumentMetadata])
def get_all_documents_metadata(db: Session = Depends(get_db), current_user: int = Depends(jwt.get_current_user)):
    """
    Returns all documents metadatas available in the application
    """
    documents = db.query(models.DocumentMetadata).all()
    return documents
