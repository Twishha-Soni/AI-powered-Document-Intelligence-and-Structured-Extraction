from fastapi import APIRouter, UploadFile, HTTPException
import tempfile, os

router = APIRouter()

@router.post('/uploads')
async def upload_document(file: UploadFile):
    if not file.filename.lower().endswith(('.pdf', '.docx', '.txt')):
        raise HTTPException(status_code=400, detail='Upload documents with extension .pdf, .docx and .txt only')

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        print('ok')
    finally:
        os.unlink(tmp_path)