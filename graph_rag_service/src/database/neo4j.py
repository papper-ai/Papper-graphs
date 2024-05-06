from neo4j import AsyncGraphDatabase, GraphDatabase, basic_auth
from neo4j.auth_management import AsyncAuthManagers, AuthManagers

from src.config import settings

auth = basic_auth(settings.neo4j_user, settings.neo4j_password)

# Holds a connection pool from which Session objects can borrow
neo4j_async_driver = AsyncGraphDatabase.driver(
    settings.neo4j_uri, auth=AsyncAuthManagers.static(auth)
)
neo4j_sync_driver = GraphDatabase.driver(
    settings.neo4j_uri, auth=AuthManagers.static(auth)
)
