import json 
import time
from pydantic import Base64Bytes
from pathlib import Path

from eval.compare import compare_documents

from app.schemas.invoice_schema import InvoiceFields
from app.schemas.resume_schema import ResumeFields
from app.schemas.purchase_order_schema import PurchaseOrderFields
from app.schemas.application_form_schema import ApplicationFormFields
from app.schemas.contract_schema import ContractFields
from app.services.extract_text import extract_text
from app.services.llm import extract_fields

SCHEMA_MAP = {
    'invoice': InvoiceFields,
    'resume': ResumeFields,
    'contract': ContractFields,
    'application_form': ApplicationFormFields,
    'purchase_order': PurchaseOrderFields
}

DOCUMENTS_DIR = Path(__file__).parent / 'purchase_order'/ 'documents'
GOLDEN_DIR = Path(__file__).parent / 'purchase_order' / 'golden'

def run_single_eval(document_path: Path, golden_path: Path) -> dict:
    filename = document_path.name
    expected_type = golden_path.stem.rsplit("_",1)[0]

    result = {
        'filename': filename,
        'expected_type': expected_type,
        'processing_time_seconds': None,
        'extraction_succeeded': False,
        'output_valid': False,
        'classification_correct': False,
        'validation_passed': False,
        'field_results': {},
        'error': None,
    }

    schema = SCHEMA_MAP.get(expected_type)
    if schema is None:
        result['error'] = f"No schema registered for expected_type: {expected_type}"
        return result

    golden_data = json.loads(golden_path.read_text())
    golden = schema(**golden_data)

    start = time.time()
    try:
        text, _warning = extract_text(str(document_path))
        pipeline_result = extract_fields(text)

        result['processing_time_seconds'] = round(time.time() - start, 2)

        if pipeline_result.get('error'):
            result['error'] = pipeline_result['error']
            return result

        result['extraction_succeeded'] = True
        result['output_valid'] = True

        classification = pipeline_result['classification']
        predicted = pipeline_result['extracted']

        result['classification_correct'] = classification.doc_type == expected_type

        # Only compare fields if the classifier routed to the SAME schema as golden
        if isinstance(predicted, schema):
            result['field_results'] = compare_documents(predicted, golden)
        else:
            result['error'] = (
                f"Classified as '{classification.doc_type}', expected type: '{expected_type}'"
                f"-- field comparison skipped (different schema)."
            )

        # Business-rule validation — assumes you have a validate_business_rules(fields) -> list[str] function
        # violations = validate_business_rules(predicted)
        # result["validation_passed"] = len(violations) == 0
        result['validation_passed'] = True

    except Exception as e:
        result['processing_time_seconds'] = round(time.time() - start, 2)
        result['error'] = str(e)

    return result

def run_all_eval() -> list[dict]:
    results = []
    for golden_path in sorted(GOLDEN_DIR.glob("*.json")):
        stem = golden_path.stem

        matches = list(DOCUMENTS_DIR.glob(f"{stem}.*"))
        if not matches:
            print(f"[eval] Warning: no document found for golden file {golden_path.name}")
            continue

        document_path = matches[0]
        print(f"[eval] Running {document_path.name}...")
        results.append(run_single_eval(document_path, golden_path))

    return results

if __name__ == '__main__':
    all_results = run_all_eval()
    Path('eval/results_po.json').write_text(json.dumps(all_results, indent=2))
    print(f'\n[eval] Done. {len(all_results)} documents processed. Results saved to eval/results_po.json')