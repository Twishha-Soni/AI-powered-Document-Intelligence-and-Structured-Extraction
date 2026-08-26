from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.models import User, Document
from app.auth.dependencies import get_current_user
from app.database.session import get_db

router = APIRouter(tags=['history'])

@router.get('/history')
def get_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> list[dict]:

    documents = (
        db.query(Document)
        .filter(Document.user_id == current_user.id)
        .order_by(Document.created_at.desc())
        .all()
    )

    return [
        {
            'document_id': d.id,
            'filename': d.filename,
            'status': d.status,
            'doc_type': d.doc_type,
            'confidence': d.confidence,
            'created_at': d.created_at
        }
        for d in documents
    ]