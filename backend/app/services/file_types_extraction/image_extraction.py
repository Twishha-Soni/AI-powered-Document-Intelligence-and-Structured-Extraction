import cv2

def extract_image_text(file_path: str, OCR_AVAILABLE: bool, ocr) -> str:
    try:
        if OCR_AVAILABLE:
            image = cv2.imread(file_path)

            result = ocr.predict(image)
            text = ''
            for res in result:
                text += f" {res["rec_texts"]}"

            return text
    
    except Exception as e:
        print(f"[image_extractor] OCR failed on image uploaded: {e}")
        return ""