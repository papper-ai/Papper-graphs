from src.database.neo4j import neo4j_sync_driver


def get_graph_view(db_name: str) -> str:
    graph_view = neo4j_sync_driver.execute_query(
        query_="MATCH (n)-[r]->(m) RETURN n.name, TYPE(r) AS relationship, m.name",
        database_=db_name,
    ).records

    return graph_view
