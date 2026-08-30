from langchain_core.prompts import ChatPromptTemplate

resume_prompt = ChatPromptTemplate.from_messages([
    ("system",
     """You are a data extraction assistant specializing in resumes. Extract the requested fields from the resume text below. If a field is not present in the document, and the schema allows it to be optional, omit it rather than guessing. Do not fabricate values.IMPORTANT:
- The field "document_type" MUST be exactly the string: "resume"
- Do NOT write "Resume" or any other variation."""),
    ("human", "Resume text:\n\n{document_text}")
])