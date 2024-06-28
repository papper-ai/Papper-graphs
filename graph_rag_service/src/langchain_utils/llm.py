from langchain_openai import ChatOpenAI as ChatAPI
from src.config import settings

llm_url = settings.remote_url + '/v1'

custom_llm = ChatAPI(
    base_url=llm_url,
    api_key="sk-not-required",
    verbose=True,
    temperature=0,
    model="suzume-llama-3-8B-multilingual-gptq-8bit",
    timeout=60*5,
    extra_body={"stop_token_ids": [128009]},
)
