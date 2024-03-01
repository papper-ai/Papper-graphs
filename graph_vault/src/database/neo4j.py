from neo4j import AsyncGraphDatabase, basic_auth
from neo4j.auth_management import AsyncAuthManagers
from src.config import settings


auth = basic_auth(settings.neo4j_user, settings.neo4j_password)

neo4j_driver = AsyncGraphDatabase.driver(
    settings.neo4j_uri, auth=AsyncAuthManagers.static(auth)
)
