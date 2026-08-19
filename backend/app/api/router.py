from fastapi import APIRouter

router = APIRouter()

from fastapi import UploadFile, HTTPException
import tempfile, os

from app.services.pdf_extractor import extract_pdf_text
from app.services.llm import extract_fields

@router.post('/uploads')
async def upload_document(file: UploadFile) -> str:
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail='Upload documents with extension .pdf only')

    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

        try:
            text, warning = extract_pdf_text(tmp_path)
            extract = extract_fields(text)
            return extract['classification'].doc_type
        finally:
            os.unlink(tmp_path)

