from fastapi import APIRouter

router = APIRouter()

from fastapi import UploadFile, HTTPException
import tempfile, os

from app.services.pdf_extractor import extract_text
from app.services.llm import extract_fields

@router.post('/uploads')
async def upload_document(file: UploadFile) -> str:
    if not file.filename.lower().endswith(('.pdf', '.docx')):
        raise HTTPException(status_code=400, detail='Upload documents with extension .pdf and .docx only')

    _, file_extension = os.path.splitext(file.filename)

    with tempfile.NamedTemporaryFile(delete=True, suffix=file_extension) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

        try:
            text, warning = extract_text(tmp_path)
            extract = extract_fields(text)
            return extract['classification'].doc_type
        finally:
            os.unlink(tmp_path)

