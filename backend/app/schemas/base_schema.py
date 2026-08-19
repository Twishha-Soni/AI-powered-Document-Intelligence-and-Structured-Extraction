from pydantic import BaseModel, Field
from typing import Literal

DocType = Literal["invoice", "resume", "purchase_order", "application_form", "contract"]

class ExtractedDocument(BaseModel):
    document_type: DocType = Field(
            description="The type of document this extraction was performed on."
        )