import pytest
import time
import json
from jsonschema import validate


TOKENS = {
    "tv": "f2373c06-47db-4d35-99f1-21e269956171",
    "mobile": "e16d0a19-dcb9-4ca0-88bc-3daed1cd393a",
    "stb": "7f34bf84-a678-4b7e-8e54-2e6d5a075225"
}


@pytest.mark.parametrize('tokens', list(TOKENS.keys()))
def test_get_single_movie(service_factory, movie_factory, tokens, session, base_url, time_valid):
    """Проверка метода get"""
    API_GET = 'api/movies'
    token = str(TOKENS[tokens])
    header = {'X-TOKEN': token}

    service = service_factory(tokens, session, base_url)
    time.sleep(5)
    movie = movie_factory(service, session, base_url, time_valid)
    time.sleep(5)
    res = session.get(url=f'{base_url}/{API_GET}', headers=header)

    assert res.status_code == 200
    for elem in res.json()['items']:
        assert elem['id'] == movie['id']


@pytest.mark.parametrize('tokens', list(TOKENS.keys()))
def test_get_single_movie_negative(service_factory, movie_factory, tokens, session, base_url, time_expires):
    """Негативный тест на запрос фильма с истекшим сроком проката"""
    API_GET = 'api/movies'
    token = str(TOKENS[tokens])
    header = {'X-TOKEN': token}

    service = service_factory(tokens, session, base_url)
    time.sleep(5)
    movie = movie_factory(service, session, base_url, time_expires)
    time.sleep(5)
    res = session.get(url=f'{base_url}/{API_GET}', headers=header)

    assert res.status_code == 200
    assert res.json() == {"items": []}


@pytest.mark.parametrize('tokens', ('3423424234234', "string", "7f34bf84-a678-4b7e-8e54"))
def test_get_broken_token(tokens, session, base_url):
    """Негативный тест на запрос фильмов с 'битым' токеном"""
    API_GET = 'api/movies'
    header = {'X-TOKEN': tokens}
    res = session.get(url=f'{base_url}/{API_GET}', headers=header)

    assert res.status_code == 403
    assert res.json()['message'] == "'Токен не найден'"


@pytest.mark.parametrize('tokens', list(TOKENS.keys()))
def test_get_multiple_movies(service_factory, movie_factory, tokens, session, base_url, time_valid):
    """Проверка метода get при получении нескольких элементов"""
    API_GET = 'api/movies'
    token = str(TOKENS[tokens])
    header = {'X-TOKEN': token}

    service = service_factory(tokens, session, base_url)
    time.sleep(5)
    for x in range(5):
        movie_factory(service, session, base_url, time_valid)
    time.sleep(5)
    res = session.get(url=f'{base_url}/{API_GET}', headers=header)

    assert res.status_code == 200
    assert len(res.json()['items']) == 5


def assert_valid_schema(data, schema_file):
    with open(schema_file) as f:
        schema = json.load(f)
    return validate(instance=data, schema=schema)


@pytest.mark.parametrize('tokens', list(TOKENS.keys()))
def test_get_scheme_validation(session, base_url, tokens, service_factory, movie_factory, time_valid):
    """Валидация схемы json"""
    API_GET = 'api/movies'
    token = str(TOKENS[tokens])
    header = {'X-TOKEN': token}

    service = service_factory(tokens, session, base_url)
    time.sleep(5)
    movie_factory(service, session, base_url, time_valid)
    time.sleep(5)
    res = session.get(url=f'{base_url}/{API_GET}', headers=header)

    assert_valid_schema(res.json(), 'todo_schema.json')


@pytest.mark.parametrize('tokens', list(TOKENS.keys()))
def test_get_multi_scheme_validation(session, base_url, tokens, service_factory, movie_factory, time_valid):
    """Валидация схемы json на нескольких объектах"""
    API_GET = 'api/movies'
    token = str(TOKENS[tokens])
    header = {'X-TOKEN': token}

    service = service_factory(tokens, session, base_url)
    time.sleep(5)
    for x in range(5):
        movie_factory(service, session, base_url, time_valid)
    time.sleep(5)
    res = session.get(url=f'{base_url}/{API_GET}', headers=header)

    assert_valid_schema(res.json(), 'todo_schema.json')
