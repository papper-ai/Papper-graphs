import logging

from src.langchain_utils.agent import initialize_agent_with_tools
from src.langchain_utils.history import construct_langchain_history
from src.qa_router.schemas import Answer, Input


async def generate_answer(input: Input) -> Answer:
    chat_history = construct_langchain_history(input.history)
    agent_executor = initialize_agent_with_tools(input.vault_id)

    response = await agent_executor.ainvoke(
        {"input": input.query, "chat_history": chat_history}
    )

    logging.info(response)

    answer = (
        response["output"]["result"]
        if isinstance(response["output"], dict)
        else response["output"]
    )

    traceback = []
    for i in range(len(response["intermediate_steps"])):
        traceback.extend(
            response["intermediate_steps"][i][1]["intermediate_steps"][0]["results"]
        )

    return Answer(answer=answer, traceback=traceback)
