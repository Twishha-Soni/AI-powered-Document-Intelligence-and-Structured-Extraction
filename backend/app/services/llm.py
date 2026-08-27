# backend/app/services/llm.py
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

from app.services.structured_call import call_structured

load_dotenv()

# ---- Dispatch table: doc_type -> (prompt_template, schema) ----
_DISPATCH = {
    "invoice": (invoice_prompt, InvoiceFields),
    "resume": (resume_prompt, ResumeFields),
    "purchase_order": (purchase_order_prompt, PurchaseOrderFields),
    "application_form": (application_form_prompt, ApplicationFormFields),
    "contract": (contract_prompt, ContractFields),
}


def _render(prompt_template, **kwargs) -> tuple[str, str]:
    messages = prompt_template.format_messages(**kwargs)
    system_text = next(m.content for m in messages if m.type == "system")
    human_text = next(m.content for m in messages if m.type == "human")
    return system_text, human_text


def _classify_document(doc_text: str) -> DocumentTypeClassification:
    system_text, human_text = _render(classification_prompt, document_text=doc_text[:100])
    return call_structured(system_text, human_text, DocumentTypeClassification)


def extract_fields(doc_text: str) -> dict:
    classification = _classify_document(doc_text)

    entry = _DISPATCH.get(classification.doc_type)
    if entry is None:
        return {
            "error": f"No extraction schema registered for document type '{classification.doc_type}'.",
            "classification": classification,
        }

    prompt_template, schema = entry
    system_text, human_text = _render(prompt_template, document_text=doc_text)
    extracted = call_structured(system_text, human_text, schema)

    return {
        "classification": classification,
        "extracted": extracted,
    }