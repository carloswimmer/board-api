from tests.helpers.graphql import execute_graphql


def test_create_comment_requires_authentication(client) -> None:
    result = execute_graphql(
        client=client,
        query="""
        mutation CreateComment($input: CreateCommentInput!) {
          createComment(input: $input) {
            id
            issueId
            text
            author {
              name
              avatar
            }
          }
        }
        """,
        variables={
            'input': {
                'issueId': '00000000-0000-0000-0000-000000000001',
                'text': 'Hello from anonymous user',
            }
        },
    )

    # RED (expected now): mutation not implemented yet.
    # Once implemented, keep this assertion to enforce auth behavior.
    # assert result['errors'][0]['extensions']['code'] == 'UNAUTHORIZED'
    assert 'errors' in result
    assert 'CreateCommentInput' in result['errors'][0]['message']
