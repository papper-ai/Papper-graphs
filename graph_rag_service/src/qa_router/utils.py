import logging

from src.langchain_utils.agent import initialize_agent_with_tools
from src.langchain_utils.history import construct_langchain_history
from src.qa_router.schemas import Answer, Input
from fastapi.exceptions import HTTPException
from neo4j.exceptions import Neo4jError


async def generate_answer(input: Input) -> Answer:
    chat_history = construct_langchain_history(input.history)
    agent_executor = initialize_agent_with_tools(input.vault_id)

    try:
        response = await agent_executor.ainvoke(
            {"input": input.query, "chat_history": chat_history}
        )
    except Neo4jError as e:
        if e.code == "Neo.ClientError.Database.DatabaseNotFound":
            logging.error(f"Database {input.vault_id} not found")
            raise HTTPException(status_code=404, detail="Graph database not found")

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
