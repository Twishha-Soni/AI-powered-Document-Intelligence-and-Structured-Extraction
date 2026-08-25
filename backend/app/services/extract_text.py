try:
    from paddleocr import PaddleOCR
    ocr = PaddleOCR(
        enable_mkldnn=False,
        use_angle_cls=False,
        use_doc_orientation_classify=False,
        use_textline_orientation=False,
        cpu_threads=2
    )
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False


from app.services.file_types_extraction.pdf_extractor import extract_pdf_text
from app.services.file_types_extraction.docx_extraction import extract_docx_text
from app.services.file_types_extraction.image_extraction import extract_image_text



def extract_text(file_path: str) -> tuple:
    if file_path.lower().endswith('.pdf'):
        return extract_pdf_text(file_path, OCR_AVAILABLE, ocr)
    if file_path.lower().endswith('.docx'):
        return extract_docx_text(file_path, OCR_AVAILABLE, ocr)
    if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
        return extract_image_text(file_path, OCR_AVAILABLE, ocr)