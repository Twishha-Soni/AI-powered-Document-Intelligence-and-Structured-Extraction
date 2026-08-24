from langchain_core.prompts import ChatPromptTemplate

application_form_prompt = ChatPromptTemplate.from_messages([
    ("system",
     """You are a data extraction assistant specializing in application form. Extract the requested fields from the application text below. If a field is not present in the document, and the schema allows it to be optional, omit it rather than guessing. Do not fabricate values."""),
    ("human", "Application form text:\n\n{document_text}")
])