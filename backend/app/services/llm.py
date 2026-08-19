from langchain_openrouter import ChatOpenRouter
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

_llm = ChatOpenRouter(
    model='google/gemma-4-31b-it:free'
)

_prompt = ChatPromptTemplate.from_template("""

""")

_chain = _prompt | _llm


def extract_fields(text: str):
    _chain.invoke(
        
    )