import docx, cv2
import numpy as np
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P

def extract_docx_text(file_path: str, OCR_AVAILABLE: bool, ocr) -> tuple:
    try:
        doc = docx.Document(file_path)

        extracted_chunks = []
        ocr_locations = []
        failed_locations = []

        para_num = 0
        table_num = 0

        for block in _iter_block_items(doc):
            if isinstance(block, Paragraph):
                para_num += 1
                text = block.text.strip()

                if text:
                    extracted_chunks.append(f"[Paragraph {para_num}]\n{text}")

                image_blobs = _get_paragraph_images(block, doc)

                for img_num, image_bytes in enumerate(image_blobs, start=1):
                    if not OCR_AVAILABLE:
                        failed_locations.append(para_num)
                        continue

                    ocr_text = _ocr_image_bytes(image_bytes, ocr)

                    if ocr_text:
                        extracted_chunks.append(f"[Paragraph {para_num} - OCR image {img_num}]\n{ocr_text}")
                        print(f"[docx_extractor] Paragaph {para_num}: OCR extractred {len(ocr_text)} chars")
                    else:
                        failed_locations.append(para_num)
                        print(f"[docx_extractor] Paragraph {para_num}: OCR returned no text")

            elif isinstance(block, Table):
                table_num += 1
                md_table = _table_to_markdown(block)

                if md_table:
                    extracted_chunks.append(f"[Table {table_num}]\n{md_table}")

        full_text = "\n\n".join(extracted_chunks)
        warning = _build_warning(ocr_locations, failed_locations, OCR_AVAILABLE)

        return full_text, warning

    except Exception as e:
        print(f"[docx_extractor] Error: {e}")
        return "","DOCX could not be read."


# --------------- Helper function ---------------

def _iter_block_items(doc):
    for child in doc.element.body.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, doc)
        elif isinstance(child, CT_Tbl):
            yield Table(child, doc)

def _table_to_markdown(table: Table) -> str:
    rows = [[cell.text.strip() for cell in row.cells] for row in table.rows]

    if not rows:
        return ''

    header, *body_rows = rows
    lines = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(["---"] * len(header)) + " |"
    ]

    for row in body_rows:
        lines.append("| " + " | ".join(row) + " |")

    return "\n".join(lines)

def _get_paragraph_images(paragraph, doc) -> list[bytes]:
    blobs = []

    for run in paragraph.runs:
        for drawing in run._element.findall(
            './/{http://schemas.openxmlformats.org/drawingml/2006/main}blip'
        ):
            r_id = drawing.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
            if r_id and r_id in doc.part.rels:
                blobs.append(doc.part.rels[r_id].target_part.blob)

    return blobs

def _ocr_image_bytes(image_bytes: bytes, ocr) -> str:
    try:
        image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
        result = ocr.predict(image)

        text_parts = []
        for res in result:
          text_parts.extend(res.get('rec_texts', []))

        return ' '.join(text_parts)

    except Exception as e:
        print(f"[docx_extractor] OCR failed: {e}")
        return ''

def _build_warning(ocr_paragraphs, failed_paragraphs, OCR_AVAILABLE):

    if not ocr_paragraphs and not failed_paragraphs:
        return ""

    parts = []
    if ocr_paragraphs:
        para_list = ", ".join(str(p) for p in ocr_paragraphs)
        parts.append(
            f"Image(s) in paragraph(s) {para_list} were processed using OCR. "
            f"Accuracy depends on image quality."
        )
    if failed_paragraphs and OCR_AVAILABLE:
        para_list = ", ".join(str(p) for p in failed_paragraphs)
        parts.append(
            f"Image(s) in paragraph(s) {para_list} could not be read even with OCR."
        )
    if failed_paragraphs and not OCR_AVAILABLE:
        para_list = ", ".join(str(p) for p in failed_paragraphs)
        parts.append(
            f"Image(s) in paragraph(s) {para_list} could not be processed because OCR is not available."
        )
    return "\n\n".join(parts)

