from langchain_community.chat_models import GigaChat

from src.config import settings

llm = GigaChat(credentials=settings.gigachat_credentials, verify_ssl_certs=False)
