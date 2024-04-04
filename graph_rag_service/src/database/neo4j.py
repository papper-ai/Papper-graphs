from neo4j import GraphDatabase, basic_auth
from neo4j.auth_management import AuthManagers

from src.config import settings

auth = basic_auth(settings.neo4j_user, settings.neo4j_password)

neo4j_driver = GraphDatabase.driver(
    settings.neo4j_uri, auth=AuthManagers.static(auth)
)
