import uuid

from fastapi import status, HTTPException, Depends, APIRouter
from ... import models, utils, jwt
from sqlalchemy.orm import Session
from ...databasecon import get_db

router = APIRouter(
    prefix="/documents/summary",
    tags=['Document Summary APIs']
)


# API to return Doc Ids who have failed extraction status
@router.get("/failed/extraction/{id}", status_code=status.HTTP_200_OK)
def get_failed_extraction_docs(id: uuid.UUID, db: Session = Depends(get_db),
                               current_user: int = Depends(jwt.get_current_user)):
    """
    This Api returns all those document IDs which have failed extraction status for
    given customer
    """
    try:
        query = db.query(models.DocumentStatus)
        query = query.with_entities(models.DocumentStatus.documentId)
        query = query.filter(
            models.DocumentStatus.customerId == id,
            models.DocumentStatus.extractionStatus == "FAILED"
        ).all()

        # separate document id value from tuple
        document_ids = [item[0] for item in query]

        # return json response
        return {'Document_Ids': document_ids}

    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=err.args[0])


# API to return count of documents for failed ingestion status
@router.get("/failed/ingestion/{id}", status_code=status.HTTP_200_OK)
def get_failed_ingestion_docs(id: uuid.UUID, db: Session = Depends(get_db),
                              current_user: int = Depends(jwt.get_current_user)):
    """
    This Api returns total count of documents which has failed ingestion status
    for given customer id
    """
    try:
        documents_with_failed_ingestion = db.query(models.DocumentStatus).filter(
            models.DocumentStatus.customerId == id,
            models.DocumentStatus.ingestionStatus == "FAILED"
        ).count()

        # return json response
        return {'total_no_of_documents': documents_with_failed_ingestion}

    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=err.args[0])


# API to return summary based on mime type
@router.get("/mimetype/{id}", status_code=status.HTTP_200_OK)
def get_mime_type_summary(id: uuid.UUID, db: Session = Depends(get_db),
                          current_user: int = Depends(jwt.get_current_user)):
    """
    This Api returns summary based on mimetype for given customer
    """
    try:
        response = []
        mime_type_ids = {}

        # get all document metadata objects for given customer
        customer_documents_metadata = utils.get_all_documents_metadata(id, db)

        # group document ids based on mimetype and update dict
        for item in customer_documents_metadata:
            if mime_type_ids.get(item[0]):
                mime_type_ids[item[0]].append(item[1])
            else:
                mime_type_ids[item[0]] = [item[1]]

        # loop through the mimetype dict
        for key, value in mime_type_ids.items():
            # fetch all related document status objects for customer using document ids fetched from metadata
            document_status_objects = utils.fetch_related_documents_status(id, db, value)

            # calculated values for response
            failed_statuses = 0
            success_statuses = 0

            # loop through document status objects to count failed and success documents
            for item in document_status_objects:
                if item[1] == models.IngestionStatusEnum.FAILED and item[2] == models.ExtractionStatusEnum.FAILED:
                    failed_statuses += 1
                elif item[1] == models.IngestionStatusEnum.SUCCEEDED and item[2] == models.ExtractionStatusEnum.SUCCEEDED:
                    success_statuses += 1

            data = {
                'mimetype': key,
                'no_of_failed_ingestion_extraction': failed_statuses,
                'no_of_success_ingestion_extraction': success_statuses,
            }

            # append object in response
            response.append(data)

        return response

    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=err.args[0])
