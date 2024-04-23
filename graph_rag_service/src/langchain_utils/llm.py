from langchain_openai import ChatOpenAI

llm_url = "http://host.docker.internal:8001/v1/"

llm = ChatOpenAI(
    base_url=llm_url,
    api_key="sk-no-key-required",
    verbose=True,
)
