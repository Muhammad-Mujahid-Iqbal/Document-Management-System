# Utility Functions

from passlib.context import CryptContext
from . import models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def pwdhasher(password: str):
    """
     JWT method to hash password
    """
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    """
        JWT method to compare and verify raw password with hashed password
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_all_documents_metadata(customer_id, db):
    """
     This method fetches all record from documents metadata for given customer id.
     It selects only mimetype and documentId
    """
    all_documents_metadata = db.query(models.DocumentMetadata).with_entities(
        models.DocumentMetadata.mimeType,
        models.DocumentMetadata.documentId,
    ).filter(
        models.DocumentMetadata.customerId == customer_id
    ).all()

    return all_documents_metadata


def fetch_related_documents_status(customer_id, db, document_ids):
    """
     This method fetches all record from documents status for given customer id
     and given document ids. It selects only id, ingestion and extraction status
    """
    all_documents_status = db.query(models.DocumentStatus).with_entities(
        models.DocumentStatus.documentId,
        models.DocumentStatus.ingestionStatus,
        models.DocumentStatus.extractionStatus
    ).filter(
        models.DocumentStatus.documentId.in_(document_ids),
        models.DocumentStatus.customerId == customer_id
    ).all()
    return all_documents_status
