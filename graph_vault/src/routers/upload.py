from fastapi import status, APIRouter

from src.database.neo4j import neo4j_driver

upload_router = APIRouter(tags=["Upload"])


@upload_router.post("/foo", status_code=status.HTTP_200_OK)
async def foo():
    async with neo4j_driver.session() as session:
        await session.run("CREATE (p:Person {name: 'Alice', age: 30})")
        result = await session.run("MATCH (n) RETURN n.name AS name")

        return {"result": await result.data()}
