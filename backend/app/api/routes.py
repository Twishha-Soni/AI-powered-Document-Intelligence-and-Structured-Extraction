from fastapi import APIRouter, UploadFile, HTTPException
import tempfile, os

from app.services.pdf_extractor import extract_pdf_text

router = APIRouter()

@router.post('/uploads')
async def upload_document(file: UploadFile) -> str:
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail='Upload documents with extension .pdf only')

    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

        return tmp_path


@router.post('/extract')
async def extract_from_document(file_path: str) -> tuple:
    if file_path:
        try:
            text, warning = extract_pdf_text(file_path)
            return text, warning
        finally:
            os.unlink(file_path)