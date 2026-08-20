from fastapi import APIRouter

router = APIRouter()

from fastapi import UploadFile, HTTPException
import tempfile, os

from app.services.extract_text import extract_text
from app.services.llm import extract_fields

@router.post('/uploads')
async def upload_document(file: UploadFile) -> dict:
    if not file.filename.lower().endswith(('.pdf', '.docx')):
        raise HTTPException(status_code=400, detail='Upload documents with extension .pdf and .docx only')

    _, file_extension = os.path.splitext(file.filename)

    with tempfile.NamedTemporaryFile(delete=True, suffix=file_extension) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

        try:
            text, warning = extract_text(tmp_path)

            if not text:
                    raise HTTPException(status_code=422, detail=warning or 'Could not extract any text from document uploaded.')
            
            return {
                 "text": text,
                 "warning": warning
            }
        
        finally:
            os.unlink(tmp_path)

@router.post("/extract")
def extract_from_document(text: str) -> dict:
    if not text:
        raise HTTPException(status_code=422, detail='Could not extract any text from document uploaded.')
    
    result = extract_fields(text)

    return {
        "classification": result["classification"].model_dump() if "classification" in result else None,
        "extracted": result["extracted"].model_dump() if "extracted" in result else None,
        "error": result.get("error"),
        "extraction_warning": warning,
    }