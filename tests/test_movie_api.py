import pytest

TOKENS = {
    "tv": "f2373c06-47db-4d35-99f1-21e269956171",
    "mobile": "e16d0a19-dcb9-4ca0-88bc-3daed1cd393a",
    "stb": "7f34bf84-a678-4b7e-8e54-2e6d5a075225"
}


@pytest.mark.parametrize('tokens', list(TOKENS.keys()))
def test_get_positive(service_factory, movie_factory, tokens, session, base_url):
    """Проверка метода get"""
    API_GET = 'api/movies'
    token = str(TOKENS[tokens])
    header = {'X-TOKEN': token}

    service = service_factory(tokens, session, base_url)
    movie = movie_factory(service, session, base_url)
    res = session.get(url=f'{base_url}/{API_GET}', headers=header)

    assert res.status_code == 200
    for elem in res.json()['items']:
        assert elem['id'] == movie['id']
