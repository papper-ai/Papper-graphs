from typing import List, Any

from qa_router.schemas import Input
from config import settings
from database.queries import search_relevant_chunks

from qa_router.schemas import Answer


def create_qa_prompt(context: str, question: str) -> str:
    return f'''
Используй следующие фрагменты контекста, чтобы ответить на вопрос в конце. Если ты не знаешь ответа, просто скажи, что ты не знаешь, не пытайся придумать ответ.

{context}

Вопрос: {question}
Полезный ответ:
    '''


async def generate_answer(input: Input):
    embedding = await create_embedding(input.query)
    result = await search_relevant_chunks(vault_id=input.vault_id, vector=embedding, top_k=2)
    qa_prompt = create_qa_prompt(context=result.text, question=input.query)
    answer = await create_completion(qa_prompt)
    return Answer(content=answer, traceback=result.search_result)


async def create_embedding(query: str) -> List[float]:
    settings.openai_client.base_url = settings.URL_TO_EMBEDDINGS
    response = await settings.openai_client.embeddings.create(input=[query], model=" ")
    return list(map(lambda x: x.embedding, response.data))[0]


async def create_completion(prompt: str) -> str:
    settings.openai_client.base_url = settings.URL_TO_LLM
    response = await settings.openai_client.completions.create(model="lightblue/suzume-llama-3-8B-multilingual",
                                                               prompt=prompt,
                                                               temperature=0.0,
                                                               max_tokens=1024)
    return response.choices[0].text.replace('<|eot_id|>', '')
