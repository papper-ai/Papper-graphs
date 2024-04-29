from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import tool

from src.langchain_utils.custom_graph_qa_chain import CustomGraphCypherQAChain
from src.langchain_utils.llm import custom_llm
from src.langchain_utils.prompts import agent_prompt, cypher_prompt, qa_prompt


class QueryKBInput(BaseModel):
    query: str = Field(description="Полный вопрос от Human.")


def initialize_agent_with_tools(graph_kb_name: str | None) -> AgentExecutor:
    @tool("query-knowledge-base-tool", args_schema=QueryKBInput, return_direct=True)
    async def query_knowledge_base(query: str) -> str:
        """Использовать базу знаний для поиска информации по вопросу Human."""

        chain = CustomGraphCypherQAChain.from_llm(
            llm=custom_llm,
            verbose=True,
            graph_kb_name=graph_kb_name,
            return_intermediate_steps=True,
            cypher_prompt=cypher_prompt,
            qa_prompt=qa_prompt,
            ssl_verify=False,
        )

        result = await chain.ainvoke(query)
        return result

    if graph_kb_name is None:
        tools = []
    else:
        tools = [query_knowledge_base]
        
    agent = create_structured_chat_agent(
        llm=custom_llm, tools=tools, prompt=agent_prompt
    )

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        return_intermediate_steps=True,
    )

    return agent_executor
