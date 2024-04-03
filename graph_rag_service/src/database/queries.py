from src.database.neo4j import neo4j_driver


async def get_graph_view() -> str:
    graph_view = neo4j_driver.execute_query(
        "MATCH (n)-[r]->(m) RETURN n.name, TYPE(r) AS relationship, m.name"
    ).records
    return graph_view
