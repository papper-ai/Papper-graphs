import langchain
from langchain_community.llms.gigachat import GigaChat
from langchain_openai import ChatOpenAI

langchain.debug = True

llm_url = "http://host.docker.internal:8001/v1/"

'''llm = ChatOpenAI(
    base_url=llm_url,
    api_key="sk-no-key-required",
    verbose=True,
    temperature=0
)'''

llm = GigaChat(verify_ssl_certs=False)
