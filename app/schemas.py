from pydantic import BaseModel, EmailStr
from datetime import datetime
from .models import RoleType, IngestionStatusEnum, ExtractionStatusEnum
import uuid


# Request/Response Schema Models for user apis and Auth Tokens
class UserBase(BaseModel):
    fname: str
    lname: str
    email: EmailStr
    role: RoleType

    class Config:
        orm_mode = True


class ReqUserCreate(UserBase):
    password: str


class RespUserCreated(UserBase):
    id: int
    created_at: datetime
    last_modified_at: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: str
    role: str


# Request/Response Schema Models for Document Metadata APIs
class ReqDocumentMetadata(BaseModel):
    customerId: uuid.UUID
    documentId: int
    documentPath: str
    documentFileName: str
    mimeType: str

    class Config:
        orm_mode = True


class ResDocumentMetadata(ReqDocumentMetadata):
    uploadedByUserId: int
    uploadedAt: datetime
    lastUpdatedAt: datetime


# Request/Response Schema Models for Document Status APIs
class ReqDocumentStatus(BaseModel):
    customerId: uuid.UUID
    documentId: int
    documentContentHash: str
    documentMetadataHash: str
    ingestionStatus: IngestionStatusEnum
    extractionStatus: ExtractionStatusEnum

    class Config:
        orm_mode = True


class ResDocumentStatus(ReqDocumentStatus):
    id: int


# Request/Response Schema Models for Customer APIs
class ReqCustomer(BaseModel):
    name: str
    company: str

    class Config:
        orm_mode = True


class ResCustomer(ReqCustomer):
    id: uuid.UUID
    created_at: datetime
    last_modified_at: datetime


# Request/Response Schema Models for Summary APIs
class ReqSummary(BaseModel):
    customerId: uuid.UUID

    class Config:
        orm_mode = True
