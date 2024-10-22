import logging

from fastapi.exceptions import HTTPException
from neo4j.exceptions import Neo4jError

from src.langchain_utils.agent import initialize_agent_with_tools
from src.langchain_utils.history import construct_langchain_history
from src.qa_router.schemas import Answer, Input


async def generate_answer(input: Input) -> Answer:
    chat_history = construct_langchain_history(input.history)
    agent_executor = initialize_agent_with_tools(graph_kb_name=input.vault_id)

    try:
        response = await agent_executor.ainvoke(
            {"input": input.query, "chat_history": chat_history}
        )
    except Neo4jError as e:
        if e.code == "Neo.ClientError.Database.DatabaseNotFound":
            logging.error(f"Database {input.vault_id} not found")
            raise HTTPException(status_code=404, detail="Graph database not found")

    logging.info(response)

    # Return the final answer if no intermediate steps were taken
    if not isinstance(response["output"], dict):
        return Answer(content=response["output"], traceback=[])
    
    # Return immediate response if tool input is broken
    if (
        response["intermediate_steps"][0][0].tool_input
        == "Invalid or incomplete response"
    ):
        return Answer(content=response["output"], traceback=[])

    # Parse taken steps from tool use into a traceback
    if isinstance(response["output"], dict):
        answer = response["output"]["result"]
        
        traceback = []
        if input.vault_id:
            for i in range(len(response["intermediate_steps"][0][1]["intermediate_steps"])):
                try:
                    traceback.extend(
                        response["intermediate_steps"][0][1]["intermediate_steps"][i][
                            "results"
                        ]
                    )
                except Exception as e:
                    logging.error(e)

            # Deduplicate traceback
            traceback = [dict(d) for d in {frozenset(d.items()) for d in traceback}]

        return Answer(content=answer, traceback=traceback)
