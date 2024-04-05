from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import tool
from src.langchain_utils.custom_graph_qa_chain import CustomGraphCypherQAChain
from src.langchain_utils.llm import llm
from src.langchain_utils.prompts import cypher_prompt, qa_prompt


chain = CustomGraphCypherQAChain.from_llm(
    llm=llm,
    verbose=True,
    return_intermediate_steps=True,
    cypher_prompt=cypher_prompt,
    qa_prompt=qa_prompt,
)


class QueryKBInput(BaseModel):
    query: str = Field(description="Вопрос пользователя")


@tool("query-knowledge-base-tool", args_schema=QueryKBInput, return_direct=True)
async def query_knowledge_base(query: str) -> str:
    """Использовать базу знаний для получения ответа на вопрос пользователя."""

    result = chain(query)
    return result
