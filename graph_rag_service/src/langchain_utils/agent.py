from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import tool
from src.langchain_utils.custom_graph_qa_chain import CustomGraphCypherQAChain
from src.langchain_utils.llm import gigachat_llm, custom_llm
from src.langchain_utils.prompts import cypher_prompt, qa_prompt, ru_prompt


class QueryKBInput(BaseModel):
    query: str = Field(description="Полный вопрос от Human.")


def initialize_agent_with_tools(graph_kb_name: str) -> AgentExecutor:
    @tool("query-knowledge-base-tool", args_schema=QueryKBInput, return_direct=True)
    async def query_knowledge_base(query: str) -> str:
        """Использовать базу знаний для поиска информации по вопросу Human."""

        chain = CustomGraphCypherQAChain.from_llm(
            llm=gigachat_llm,
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
        llm=custom_llm, tools=[query_knowledge_base], prompt=ru_prompt
    )

    agent_executor = AgentExecutor(
        agent=agent,
        tools=[query_knowledge_base],
        verbose=True,
        handle_parsing_errors=True,
        return_intermediate_steps=True,
        max_iterations=7
    )

    return agent_executor
