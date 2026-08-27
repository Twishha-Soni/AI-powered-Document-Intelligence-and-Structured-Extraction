from fastapi import APIRouter, Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.services.llm import extract_fields
from app.database.models import User, Document
from app.database.session import get_db
from app.auth.dependencies import get_current_user


router = APIRouter(tags=['extract'])


@router.post("/extract/{document_id}")
def extract_from_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> dict:

    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
        ).first()
    
    if document is None:
        raise HTTPException(status_code=422, detail='Document not found.')
    
    result = extract_fields(document.extracted_text)

    if 'error' in result and result['error']:
        raise HTTPException(status_code=422, detail=result['error'])

    classification = result['classification']
    extracted = result['extracted']

    document.status = 'extracted'
    document.doc_type = classification.doc_type
    document.confidence = classification.confidence
    document.extracted_data = extracted.model_dump()

    db.commit()
    db.refresh(document)

    return {
        "document_id": document.id,
        "status": document.status,
        "doc_type": document.doc_type,
        "confidence": document.confidence * 100,
        "extracted": document.extracted_data,
    }