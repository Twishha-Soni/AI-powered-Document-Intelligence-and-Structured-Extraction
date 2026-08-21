from pydantic import BaseModel, Field

from app.schemas.base_schema import DocType

class DocumentTypeClassification(BaseModel):
    doc_type: DocType = Field(
        description="Best-guess classification of the document's type."
    )
    confidence: float = Field(
        ge=0.0, le=1.0,
        description="Model's confidence in this classification, from 0 to 1."
    )