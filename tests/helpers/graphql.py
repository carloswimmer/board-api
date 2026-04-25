from __future__ import annotations

from typing import Any


def execute_graphql(
    client: Any,
    query: str,
    variables: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
) -> dict[str, Any]:
    response = client.post(
        '/graphql',
        json={
            'query': query,
            'variables': variables or {},
        },
        headers=headers or {},
    )
    return response.json()
