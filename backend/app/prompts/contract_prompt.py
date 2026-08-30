from langchain_core.prompts import ChatPromptTemplate

contract_prompt = ChatPromptTemplate.from_messages([
    ("system",
     """You are a data extraction assistant specializing in contracts. Extract the requested fields from the contract text below. If a field is not present in the document, and the schema allows it to be optional, omit it rather than guessing. Do not fabricate values.IMPORTANT:
- The field "document_type" MUST be exactly the string: "contract"
- Do NOT write "Contract" or any other variation."""),
    ("human", "Contract text:\n\n{document_text}")
])