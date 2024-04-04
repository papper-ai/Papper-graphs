from typing import List

from langchain_core.messages import AIMessage, HumanMessage
from src.qa_router.schemas import Message, Role


def construct_langchain_history(
    history: List[Message],
) -> List[HumanMessage | AIMessage]:
    chat_history = []
    for message in history:
        if message.role == Role.USER:
            chat_history.append(HumanMessage(content=message["content"]))
        elif message.role == Role.AI:
            chat_history.append(AIMessage(content=message["content"]))
    return chat_history
