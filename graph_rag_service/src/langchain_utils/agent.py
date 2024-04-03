from langchain.agents import AgentExecutor, create_structured_chat_agent
from src.langchain_utils.llm import llm
from src.langchain_utils.prompts import ru_prompt
from src.langchain_utils.tools import query_knowledge_base

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
