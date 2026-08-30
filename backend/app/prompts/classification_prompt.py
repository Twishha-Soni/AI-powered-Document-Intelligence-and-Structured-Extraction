from langchain_core.prompts import ChatPromptTemplate

classification_prompt = ChatPromptTemplate.from_messages([
    ("system",
     """You are a document classification assistant. Given the extracted text of a document, determine which of the following types it is: invoice, resume, purchase_order, application_form, or contract.Base your decision on structural and content cues (headings, terminology, layout patterns) rather than assuming from a single keyword. If the document doesn't clearly match any type reflect your uncertainty in the confidence score. Do not output any explanation. Just type as 'unknown' rather than from above options given and score."""),
    ("human", "Document text:\n\n{document_text}")
])
