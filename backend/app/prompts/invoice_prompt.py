from langchain_core.prompts import ChatPromptTemplate

invoice_prompt = ChatPromptTemplate.from_messages([
    ("system",
     """You are a data extraction assistant specializing in invoices. Extract the requested fields from the invoice text below. If a field is not present in the document, and the schema allows it to be optional, omit it rather than guessing. Do not fabricate values.IMPORTANT:
- The field "document_type" MUST be exactly the string: "invoice"
- Do NOT write "Invoice" or any other variation."""),
    ("human", "Invoice text:\n\n{document_text}")
])