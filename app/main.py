from fastapi import FastAPI
from strawberry.asgi import GraphQL

from app.graphql.schema import schema

app = FastAPI(title="board-api", version="0.1.0")

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

graphql_app = GraphQL(schema)
app.mount("/graphql", graphql_app)
