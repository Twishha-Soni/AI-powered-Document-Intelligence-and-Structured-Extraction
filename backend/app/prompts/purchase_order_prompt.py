from langchain_core.prompts import ChatPromptTemplate

purchase_order_prompt = ChatPromptTemplate.from_messages([
    ("system",
     """You are a data extraction assistant specializing in purchase order. Extract the requested fields from the purchase order text below. If a field is not present in the document, and the schema allows it to be optional, omit it rather than guessing. Do not fabricate values.IMPORTANT:
- The field "document_type" MUST be exactly the string: "purchase_order"
- Do NOT write "Purchase Order" or any other variation."""),
    ("human", "Purchase order text:\n\n{document_text}")
])