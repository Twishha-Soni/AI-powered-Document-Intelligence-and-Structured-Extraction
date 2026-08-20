try:
    from paddleocr import PaddleOCR
    ocr = PaddleOCR(enable_mkldnn=False)
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False


from app.services.pdf_extractor import extract_pdf_text
from app.services.docx_extraction import extract_docx_text



def extract_text(file_path: str) -> tuple:
    if file_path.lower().endswith('.pdf'):
        return extract_pdf_text(file_path, OCR_AVAILABLE, ocr)
    if file_path.lower().endswith('.docx'):
        return extract_docx_text(file_path, OCR_AVAILABLE, ocr)