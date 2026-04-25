from tests.helpers.graphql import execute_graphql


def test_graphql_ping_returns_pong(client) -> None:
    result = execute_graphql(
        client=client,
        query="""
        query {
          ping
        }
        """,
    )

    assert 'errors' not in result
    assert result['data']['ping'] == 'pong'
