from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text
from strawberry.asgi import GraphQL

from app.db.session import engine
from app.graphql.schema import schema


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    with engine.connect() as conn:
        conn.execute(text('SELECT 1'))
    yield


app = FastAPI(title='board-api', version='0.1.0', lifespan=lifespan)


@app.get('/health')
def health() -> dict[str, str]:
    return {'status': 'ok'}


graphql_app = GraphQL(schema)
app.mount('/graphql', graphql_app)
