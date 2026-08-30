import os
import logging
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

from app.prompts.classification_prompt import classification_prompt
from app.prompts.invoice_prompt import invoice_prompt
from app.prompts.application_form_prompt import application_form_prompt
from app.prompts.contract_prompt import contract_prompt
from app.prompts.resume_prompt import resume_prompt
from app.prompts.purchase_order_prompt import purchase_order_prompt

from app.schemas.classification_schema import DocumentTypeClassification
from app.schemas.invoice_schema import InvoiceFields
from app.schemas.application_form_schema import ApplicationFormFields
from app.schemas.contract_schema import ContractFields
from app.schemas.resume_schema import ResumeFields
from app.schemas.purchase_order_schema import PurchaseOrderFields

load_dotenv()

logger = logging.getLogger(__name__)

# ---------- LLM ----------
_llm = init_chat_model(
    model=os.getenv("MODEL"),
    model_provider="google_genai",          # free Gemini API
    api_key=os.getenv("GOOGLE_API_KEY"),
    timeout=60,
    max_retries=3,
)

_classification_chain = classification_prompt | _llm.with_structured_output(DocumentTypeClassification)

# ---- Dispatch table: doc_type -> (prompt, schema) ----
_DISPATCH = {
    "invoice": (invoice_prompt, InvoiceFields),
    "resume": (resume_prompt, ResumeFields),
    "purchase_order": (purchase_order_prompt, PurchaseOrderFields),
    "application_form": (application_form_prompt, ApplicationFormFields),
    "contract": (contract_prompt, ContractFields),
}


def _classify_document(doc_text: str) -> DocumentTypeClassification:
    """Classify the document. Raises on failure so caller can handle it."""
    return _classification_chain.invoke(
        {"document_text": doc_text[:300]}  
    )

def extract_fields(doc_text: str) -> dict:
    if not doc_text or not doc_text.strip():
        return {
            "error": "Empty document text provided.",
            "classification": None,
            "extracted": None,
        }

    # 1. Classification
    try:
        classification = _classify_document(doc_text)
        logger.info(f"Document classified as: {classification.doc_type}")
    except Exception as e:
        logger.error(f"Classification failed: {e}", exc_info=True)
        return {
            "error": "Failed to classify document",
            "details": str(e),
            "classification": None,
            "extracted": None,
        }

    # 2. Look up extraction pipeline
    entry = _DISPATCH.get(classification.doc_type)
    if entry is None:
        logger.warning(f"No schema registered for doc_type='{classification.doc_type}'")
        return {
            "error": f"No extraction schema registered for document type '{classification.doc_type}'.",
            "classification": classification,
            "extracted": None,
        }

    prompt, schema = entry

    # 3. Extraction
    try:
        extraction_chain = prompt | _llm.with_structured_output(schema)
        extracted = extraction_chain.invoke({"document_text": doc_text})
        logger.info("Fields extracted successfully.")
    except Exception as e:
        logger.error(f"Extraction failed for {classification.doc_type}: {e}", exc_info=True)
        return {
            "error": f"Failed to extract fields for document type '{classification.doc_type}'",
            "details": str(e),
            "classification": classification,
            "extracted": None,
        }

    return {
        "classification": classification,
        "extracted": extracted,
        "error": None,
    }