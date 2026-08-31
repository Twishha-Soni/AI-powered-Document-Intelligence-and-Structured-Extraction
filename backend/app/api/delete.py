from fastapi import APIRouter, Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.database.models import User, Document
from app.database.session import get_db
from app.auth.dependencies import get_current_user


router = APIRouter(tags=['delete'])

@router.delete("/document/{document_id}")
def delete_document(
    document_id: int, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> dict:
    
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()

    if document is None:
        raise HTTPException(status_code=404, detail="Document not found.")

    db.delete(document)
    db.commit()

    return {
        'Success': 'Document is deleted succesfully.'
    }