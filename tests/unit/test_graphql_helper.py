from tests.helpers.graphql import execute_graphql


class DummyResponse:
    def __init__(self, payload):
        self._payload = payload

    def json(self):
        return self._payload


class DummyClient:
    def __init__(self):
        self.last_path = None
        self.last_json = None
        self.last_headers = None

    def post(self, path, json, headers):
        self.last_path = path
        self.last_json = json
        self.last_headers = headers
        return DummyResponse({'data': {'ok': True}})


def test_execute_graphql_posts_expected_payload() -> None:
    client = DummyClient()

    result = execute_graphql(
        client=client,
        query='query { ping }',
        variables={'a': 1},
        headers={'x-test': '1'},
    )

    assert client.last_path == '/graphql'
    assert client.last_json == {'query': 'query { ping }', 'variables': {'a': 1}}
    assert client.last_headers == {'x-test': '1'}
    assert result == {'data': {'ok': True}}


def test_execute_graphql_uses_defaults() -> None:
    client = DummyClient()

    result = execute_graphql(
        client=client,
        query='query { ping }',
    )

    assert client.last_json == {'query': 'query { ping }', 'variables': {}}
    assert client.last_headers == {}
    assert result == {'data': {'ok': True}}
