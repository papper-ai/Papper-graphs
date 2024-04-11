from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import tool
from src.langchain_utils.custom_graph_qa_chain import CustomGraphCypherQAChain
from src.langchain_utils.llm import llm
from src.langchain_utils.prompts import cypher_prompt, qa_prompt, ru_prompt


class QueryKBInput(BaseModel):
    query: str = Field(description="Вопрос пользователя")


def initialize_agent_with_tools(graph_kb_name: str) -> AgentExecutor:
    @tool("query-knowledge-base-tool", args_schema=QueryKBInput, return_direct=True)
    async def query_knowledge_base(query: str) -> str:
        """Использовать базу знаний для получения ответа на вопрос пользователя."""

        chain = CustomGraphCypherQAChain.from_llm(
            llm=llm,
            verbose=True,
            graph_kb_name=graph_kb_name,
            return_intermediate_steps=True,
            cypher_prompt=cypher_prompt,
            qa_prompt=qa_prompt,
            ssl_verify=False,
        )

        result = await chain.ainvoke(query)
        return result

    agent = create_structured_chat_agent(
        llm=llm, tools=[query_knowledge_base], prompt=ru_prompt
    )

    agent_executor = AgentExecutor(
        agent=agent,
        tools=[query_knowledge_base],
        verbose=True,
        handle_parsing_errors=True,
        return_intermediate_steps=True,
    )

    return agent_executor
