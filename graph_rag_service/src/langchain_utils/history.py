from typing import List

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from src.langchain_utils.prompts import SYSTEM_PROMPT
from src.qa_router.schemas import Message, Role


def construct_langchain_history(
    history: List[Message],
) -> List[HumanMessage | AIMessage]:
    chat_history = []
    chat_history.append(SystemMessage(content=SYSTEM_PROMPT))

    for message in history:
        if message.role == Role.USER:
            chat_history.append(HumanMessage(content=message.content))
        elif message.role == Role.AI:
            chat_history.append(AIMessage(content=message.content))
    return chat_history
