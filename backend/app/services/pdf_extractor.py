import fitz, cv2

try:
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    

def extract_pdf_text(file_path: str) -> tuple:
    try:
        with fitz.open(file_path) as doc:

            extracted_pages = []
            ocr_pages = []
            failed_pages = []

            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text().strip()

                if text:
                    extracted_pages.append(f"[Page {page_num + 1}]\n{text}")

                else:
                    if OCR_AVAILABLE:
                        ocr_text = _ocr_page(page, page_num + 1)
                        if ocr_text:
                            text = " ".join(ocr_text)
                            extracted_pages.append(f"[Page {page_num + 1} - OCR]\n{text}")
                            ocr_pages.append(page_num + 1)
                            print(f"[pdf_extractor] Page {page_num + 1}: OCR extracted {len(ocr_text)} chars)")
                        else:
                            failed_pages.append(page_num + 1)
                            print(f"[pdf_extractor] Page {page_num + 1}: OCR returned no text")
                    else:
                        failed_pages.append(page_num + 1)

        full_text = "\n\n".join(extracted_pages)
        warning = _build_warning(ocr_pages, failed_pages, OCR_AVAILABLE)

        return full_text, warning

    except Exception as e:
        print(f"[pdf_extractor] Error: {e}")
        return "","PDF could not be read."


# ---- Helper function ----
def _ocr_page(page, page_num: int) -> str:
    try:
        image = cv2.imread(page)

        data = pytesseract.image_to_data(
            image, 
            output_type=pytesseract.Output.DICT
        )

        for i, text in enumerate(data["text"]):

            if not text.strip():
                continue

            x = data["left"][i]
            y = data["top"][i]
            w = data["width"][i]
            h = data["height"][i]

            cv2.rectangle(
                image,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

            cv2.imwrite(f"/home/twishhasoni/ocr_boxes_{page}.png", image)

            return data['text']
    except Exception as e:
        print(f"[pdf_extractor] OCR failed on page {page_num}: {e}")
        return ""

def _build_warning(ocr_pages: list, failed_pages: list, ocr_available: bool) -> str:
    if not ocr_pages and not failed_pages:
        return ""

    parts = []

    if ocr_pages:
        page_list = ", ".join(str(p) for p in ocr_pages)
        parts.append(
            f"Page(s) {page_list} were image-based and were processed using OCR. "
            f"Accuracy depends on image quality."
        )

    if failed_pages and ocr_available:
        page_list = ", ".join(str(p) for p in failed_pages)
        parts.append(
            f"Page(s) {page_list} could not be read even with OCR "
            f"(possibly blank or very low quality images)."
        )

    if failed_pages and not ocr_available:
        page_list = ", ".join(str(p) for p in failed_pages)
        parts.append(
            f"Page(s) {page_list} are image-based but Tesseract OCR is not installed. "
            f"Install it with: uv add pytesseract && apt install tesseract-ocr"
        )

    return "\n\n".join(parts)