import typing

import langchain_core
from langchain.prompts.prompt import PromptTemplate
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)

CYPHER_GENERATION_TEMPLATE = """Твоя задача - найти в схеме графа вершинs, чтобы получить о них информацию для ответа на вопрос. Ты должен основываться на предоставленной схеме графа и следовать инструкциям ниже:
1. Напиши имена вершин в формате списка, например ["вершина1", "вершина2"] без каких-либо других символов;
2. Используй ТОЛЬКО вершины, УПОМЯНУТЫЕ В СХЕМЕ ГРАФА.
3. Список должен состоять из НЕ БОЛЕЕ, чем 3 вершин.

Схема графа:
{schema}

Вопрос: {question}

Имена вершин:"""

cypher_prompt = PromptTemplate(
    template=CYPHER_GENERATION_TEMPLATE, input_variables=["schema", "question"]
)


CYPHER_QA_TEMPLATE = """Ты помощник, который помогает формировать приятные и понятные для человека ответы.
Ты имеешь информацию, которую ты должен использовать для построения ответа, но только если она релевантна вопросу.
Найденная информация является авторитетной, ты никогда не должен сомневаться в ней или пытаться использовать свои внутренние знания для ее исправления.
Если найденная информация пуста, сообщи, что информации не найдено.
Финальный ответ должен быть легко читаемым, структурированным и полезным.

Информация:
{context}

Вопрос:
{question}

Напиши полезный ответ:"""

qa_prompt = PromptTemplate(
    input_variables=["context", "question"], template=CYPHER_QA_TEMPLATE
)


AGENT_PROMPT_TEMPLATE = """Ты должен ответить на вопрос Human максимально полезно и точно. У тебя есть доступ к инструменту, который называется "query-knowledge-base-tool":
{tools}

Больше никаких инструментов нет. Вызывай этот инструмент, чтобы найти ответ по базе знаний. Если по базе знаний ничего не нашлось, попробуй вызвать инструмент снова, а потом ответь самостоятельно, упомянув, что не нашел информации в базе.
Ты также можешь сразу дать ответ, для этого передай значение для ключа "action": "Final Answer".

Используй JSON-объект для указания инструмента, предоставив значение для ключа "action": "query-knowledge-base-tool" и значение для ключа "action_input" (ввод для "query-knowledge-base-tool").

Таким образом, допустимые значения "action": "Final Answer" или "query-knowledge-base-tool"

Предоставляй только ОДНО действие в $JSON_BLOB, как показано:
```
{{
  "action": $TOOL_NAME,
  "action_input": $INPUT
}}
```

Следуй этому формату:

Question: входящий вопрос для ответа
Thought: учитывайте предыдущие и последующие шаги
Action:
```
$JSON_BLOB
```
Observation: результат действия
... (повтори Question/Action/Thought N раз)
Thought: Я знаю, что ответить.
Action:
```
{{
  "action": "Final Answer",
  "action_input": "Финальный ответ человеку"
}}

Начинай! Помни, что ВСЕГДА нужно отвечать действительным json-объектом для одного действия. Не используй форматированный вывод. Используй инструменты при необходимости. Отвечай мне напрямую, если это уместно. Формат - Action:```$JSON_BLOB```затем Observation\n\n"""

(
    agent_prompt := ChatPromptTemplate(
        input_variables=["agent_scratchpad", "input", "tool_names", "tools"],
        input_types={
            "chat_history": typing.List[
                typing.Union[
                    langchain_core.messages.ai.AIMessage,
                    langchain_core.messages.human.HumanMessage,
                    langchain_core.messages.chat.ChatMessage,
                    langchain_core.messages.system.SystemMessage,
                    langchain_core.messages.function.FunctionMessage,
                    langchain_core.messages.tool.ToolMessage,
                ]
            ]
        },
        metadata={
            "lc_hub_owner": "hwchase17",
            "lc_hub_repo": "structured-chat-agent",
            "lc_hub_commit_hash": "ea510f70a5872eb0f41a4e3b7bb004d5711dc127adee08329c664c6c8be5f13c",
        },
        messages=[
            SystemMessagePromptTemplate(
                prompt=PromptTemplate(
                    input_variables=["tool_names", "tools"],
                    template='Respond to the human as helpfully and accurately as possible. You have access to the following tools:\n\n{tools}\n\nUse a json blob to specify a tool by providing an action key (tool name) and an action_input key (tool input).\n\nValid "action" values: "Final Answer" or {tool_names}\n\nProvide only ONE action per $JSON_BLOB, as shown:\n\n```\n{{\n  "action": $TOOL_NAME,\n  "action_input": $INPUT\n}}\n```\n\nFollow this format:\n\nQuestion: input question to answer\nThought: consider previous and subsequent steps\nAction:\n```\n$JSON_BLOB\n```\nObservation: action result\n... (repeat Thought/Action/Observation N times)\nThought: I know what to respond\nAction:\n```\n{{\n  "action": "Final Answer",\n  "action_input": "Final response to human"\n}}\n\nBegin! Reminder to ALWAYS respond with a valid json blob of a single action. Use tools if necessary. Respond directly if appropriate. Format is Action:```$JSON_BLOB```then Observation',
                )
            ),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            HumanMessagePromptTemplate(
                prompt=PromptTemplate(
                    input_variables=["agent_scratchpad", "input"],
                    template="{input}\n\n{agent_scratchpad}\n (reminder to respond in a JSON blob no matter what)",
                )
            ),
        ],
    )
).messages[0].prompt.template = AGENT_PROMPT_TEMPLATE

SYSTEM_PROMPT = """Ты - интеллектуальный помощник по имени Papper, который отвечает на вопросы по документам пользователя."""
