from tests.helpers.graphql import execute_graphql


def test_issues_query_returns_grouped_status_buckets(client) -> None:
    result = execute_graphql(
        client=client,
        query="""
        query {
          issues {
            backlog { id issueNumber title status comments }
            todo { id issueNumber title status comments }
            inProgress { id issueNumber title status comments }
            done { id issueNumber title status comments }
          }
        }
        """,
    )

    # RED (expected now): schema still doesn't expose `issues`
    assert 'errors' not in result
    assert result['data']['issues'] == {
        'backlog': [],
        'todo': [],
        'inProgress': [],
        'done': [],
    }
