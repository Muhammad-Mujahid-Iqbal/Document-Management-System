from sqlalchemy import Column, Integer, String, UniqueConstraint, Enum, func, DateTime
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .databasecon import Base
import enum
from sqlalchemy.dialects.postgresql import UUID
import uuid


class RoleType(enum.Enum):
    """
    User Role Type Enum Class
    """
    developer = "developer"
    admin = "admin"


class IngestionStatusEnum(enum.Enum):
    """
        Document Status's Ingestion Enum Class
    """
    STARTED = "STARTED"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"


class ExtractionStatusEnum(enum.Enum):
    """
    Document Status's Extraction Enum Class
    """
    STARTED = "STARTED"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"


class User(Base):
    """
    Model class for main User database table
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    fname = Column(String, nullable=False)
    lname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(Enum(RoleType), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    last_modified_at = Column(DateTime(
        timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())


class Customer(Base):
    """
     Model class for customer database table
    """
    __tablename__ = "customers"
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    name = Column(String, nullable=False)
    company = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    last_modified_at = Column(DateTime(
        timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())


class DocumentMetadata(Base):
    """
    Model class for document metadata database table
    """
    __tablename__ = "document_metadata"
    __table_args__ = (UniqueConstraint('customerId', 'documentId'),)
    id = Column(Integer, primary_key=True, nullable=False)
    customerId = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False, index=True)
    documentId = Column(Integer, nullable=False, index=True)
    documentPath = Column(String, nullable=False)
    documentFileName = Column(String, nullable=False)
    mimeType = Column(String, nullable=False)
    uploadedAt = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    lastUpdatedAt = Column(DateTime(
        timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    uploadedByUserId = Column(Integer, ForeignKey("users.id"), nullable=False)


class DocumentStatus(Base):
    """
    Model class for document status database table
    """
    __tablename__ = "document_status"
    __table_args__ = (UniqueConstraint('customerId', 'documentId'),)
    id = Column(Integer, primary_key=True, nullable=False)
    customerId = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False, index=True)
    documentId = Column(Integer, nullable=False, index=True)
    documentContentHash = Column(String, nullable=False)
    documentMetadataHash = Column(String, nullable=False)
    ingestionStatus = Column(Enum(IngestionStatusEnum), nullable=False)
    extractionStatus = Column(Enum(ExtractionStatusEnum), nullable=False)
    logs = Column(String, nullable=True)
