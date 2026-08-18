from fastapi import APIRouter, UploadFile, HTTPException
import tempfile, os

from app.services.pdf_extractor import extract_pdf_text

router = APIRouter()

@router.post('/uploads')
async def upload_document(file: UploadFile) -> tuple:
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail='Upload documents with extension .pdf only')

    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        text, warning = extract_pdf_text(tmp_path)
        return text, warning
    finally:
        os.unlink(tmp_path)