from langchain.graphs import Neo4jGraph
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import tool
from langchain_community.chat_models import GigaChat

from src.config import settings
from src.langchain_utils.custom_graph_qa_chain import CustomGraphCypherQAChain
from src.langchain_utils.prompts import cypher_prompt, qa_prompt

graph = Neo4jGraph(
    url=settings.neo4j_uri,
    username=settings.neo4j_user,
    password=settings.neo4j_password,
)

llm = GigaChat(credentials=settings.gigachat_credentials, verify_ssl_certs=False)

chain = CustomGraphCypherQAChain.from_llm(
    llm=llm,
    graph=graph,
    verbose=True,
    return_intermediate_steps=True,
    cypher_prompt=cypher_prompt,
    qa_prompt=qa_prompt,
    validate_cypher=True,
)


class QueryKBInput(BaseModel):
    query: str = Field(description="Вопрос пользователя")


@tool("query-knowledge-base-tool", args_schema=QueryKBInput, return_direct=True)
def query_knowledge_base(query: str) -> str:
    """Использовать базу знаний для получения ответа на вопрос пользователя."""

    result = chain(query)
    return result
