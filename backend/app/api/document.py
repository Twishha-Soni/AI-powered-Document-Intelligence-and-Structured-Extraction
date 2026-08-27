from fastapi import APIRouter, Depends
from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Any

from app.services.llm import extract_fields
from app.database.models import User, Document
from app.database.session import get_db
from app.auth.dependencies import get_current_user


router = APIRouter(tags=['document'])

class DocumentSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    filename: str
    status: str
    extracted_text: str | None = None
    doc_type: str | None = None
    confidence: float | None = None
    extracted_data: dict[str, Any] | None = None
    created_at: datetime

@router.get("/document/{document_id}",response_model=DocumentSchema)
def get_document(
    document_id: int, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> DocumentSchema:
    
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()

    if document is None:
        raise HTTPException(status_code=404, detail="Document not found.")

    detail = DocumentSchema.model_validate(document)
    if detail.confidence is not None:
        detail.confidence *= 100

    return document