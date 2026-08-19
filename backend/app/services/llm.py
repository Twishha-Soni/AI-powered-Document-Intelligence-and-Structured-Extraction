from langchain_openrouter import ChatOpenRouter
from dotenv import load_dotenv

from app.prompts.classification_prompt import classification_prompt
from app.prompts.invoice_prompt import invoice_prompt
from app.schemas.classification_schema import DocumentTypeClassification
from app.schemas.invoice_schema import InvoiceFields

load_dotenv()

_llm = ChatOpenRouter(
    model='gpt-5-nano'
)

_classification_chain = classification_prompt | _llm.with_structured_output(DocumentTypeClassification)


def _classify_document(doc_text: str) -> DocumentTypeClassification:
    return _classification_chain.invoke(
        {'document_text': doc_text}
    )

# ---- Dispatch table: doc_type -> (prompt, schema) ----
_DISPATCH = {
    "invoice": (invoice_prompt, InvoiceFields),
    # "resume": (resume_prompt, ResumeFields),
    # "purchase_order": (po_prompt, PurchaseOrderFields),
    # "application_form": (application_form_prompt, ApplicationFormFields),
    # "contract": (contract_prompt, ContractFields),
}

def extract_fields(doc_text: str) -> dict:
    classification = _classify_document(doc_text)

    entry = _DISPATCH.get(classification.doc_type)
    if entry is None:
        return {
            "error": f"No extraction schema registered for document type '{classification.doc_type}'.",
            "classification": classification,
        }

    prompt, schema = entry
    extraction_chain = prompt | _llm.with_structured_output(schema)
    extracted = extraction_chain.invoke({'document_text': doc_text})

    return {
        'classification': classification,
        'extracted': extracted
    }