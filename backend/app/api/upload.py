from fastapi import APIRouter, Depends
from fastapi import UploadFile, HTTPException
import tempfile, os
from sqlalchemy.orm import Session

from app.services.extract_text import extract_text
from app.database.models import User, Document
from app.auth.dependencies import get_current_user
from app.database.session import get_db

router = APIRouter(tags=['upload'])


@router.post('/uploads')
async def upload_document(
     file: UploadFile,
     current_user: User = Depends(get_current_user),
     db: Session = Depends(get_db)
) -> dict:
    
    if not file.filename.lower().endswith(('.pdf', '.docx', '.png', '.jpg', '.jpeg', '.webp')):
        raise HTTPException(status_code=400, detail='Upload documents with extension .pdf and .docx only')

    _, file_extension = os.path.splitext(file.filename)

    with tempfile.NamedTemporaryFile(delete=True, suffix=file_extension) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

        try:
            text, warning = extract_text(tmp_path)

            if not text:
                    raise HTTPException(status_code=422, detail=warning or 'Could not extract any text from document uploaded.')

            document = Document(
                 user_id=current_user.id,
                 filename=file.filename,
                 status='uploaded',
                 extracted_text=text
            )

            db.add(document)
            db.commit()
            db.refresh(document)
            
            return {
                 "text": text,
                 'document_id': document.id,
                 'status': document.status,
                 "warning": warning
            }
        
        finally:
            os.unlink(tmp_path)