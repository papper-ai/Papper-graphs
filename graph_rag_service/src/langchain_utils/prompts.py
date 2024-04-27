from langchain import hub
from langchain.prompts.prompt import PromptTemplate

CYPHER_GENERATION_TEMPLATE = """Твоя задача - составить запрос Cypher по шаблону, чтобы получить информацию по вопросу. Ты должен основываться на предоставленной схеме графа и следовать инструкциям ниже:

1. Напиши только запрос Cypher по шаблону. Запрос должен получать связи от вершины, упомянутой в схеме;
2. Используй ТОЛЬКО вершины, УПОМЯНУТЫЕ В СХЕМЕ ГРАФА. Никогда не подставляй вершины, которая не упомянуты в данной схеме.

Шаблон для запроса:
MATCH (a)-[r]-(b) WHERE a.name = 'имя_вершины' RETURN r

Используй ТОЛЬКО ЭТОТ ШАБЛОН. Вместо 'имя_вершины' ты должен вставить присутствующую в схеме и подходящую под вопрос вершину графа в нижнем регистре. Запрос больше никак НЕЛЬЗЯ ИЗМЕНЯТЬ И НЕЛЬЗЯ ДОПОЛНЯТЬ.

Схема графа:
{schema}

Вопрос: {question}

Cypher запрос:"""

'''
CYPHER_GENERATION_TEMPLATE = """You are an expert who creates Cypher queries to get information for a given question based on the Graph Schema provided, following the instructions below:
1. Generate one Cypher query and nothing else;
2. Use one node that is present in the schema provided and is relevant to the given question, like this:

"MATCH (n)-[r]-(m)
WHERE n.name = 'node_name'
RETURN r

Put the name of a node in the query instead of 'node_name'. 'node_name' should be exactly taken from the schema, just like it is. Never change it.


Graph Schema:
{schema}

Question: {question}

Query:"""'''

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

'''CYPHER_QA_TEMPLATE = """You are an assistant that helps to form nice and human understandable answers.
The information part contains the provided information that you must use to construct an answer.
The provided information is authoritative, you must never doubt it.
Make the answer sound as a response to the question. Do not mention that you based the result on the given information.
If the provided information is empty, say that you don't know the answer, but still answer from your own knowledge.
Final answer should be easily readable and structured. It should be written fully in the language of the provided question.
Information:
{context}

Question: {question}
Helpful Answer:"""'''

qa_prompt = PromptTemplate(
    input_variables=["context", "question"], template=CYPHER_QA_TEMPLATE
)


RU_PROMPT_TEMPLATE = """Ты должен ответить на вопрос Human максимально полезно и точно. У тебя есть доступ к инструменту, который называется "query-knowledge-base-tool":
{tools}

Больше никаких инструментов нет. Вызывай этот инструмент, чтобы найти ответ по базе знаний. Если по базе знаний ничего не нашлось, попробуй еще, а потом ответь самостоятельно.
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

# Change pre-made prompt template to Russian
(ru_prompt := hub.pull("hwchase17/structured-chat-agent")).messages[
    0
].prompt.template = RU_PROMPT_TEMPLATE

# ru_prompt = hub.pull("hwchase17/structured-chat-agent")

SYSTEM_PROMPT = """Ты - интеллектуальный помощник по имени Papper, который отвечает на вопросы по документам пользователя."""
