import pytest
import requests
import time


def pytest_addoption(parser):
    parser.addoption(
        "--url",
        action="store",
        default="http://qa-test.iptv.rt.ru:4000",
        help="Request base url"
    )


@pytest.fixture(scope="module")
def base_url(request):
    return request.config.getoption("--url")


@pytest.fixture(scope="module")
def session():
    return requests.Session()


@pytest.fixture
def service_factory(session, base_url, request):
    API_SERVICE = 'qa/services'

    def fin():
        session.delete(url=f'{base_url}/{API_SERVICE}')

    def _service_factory(token, session, base_url):
        """Creates service for given token"""

        payload = {
            "id": 0,
            "name": "subscription",
            "description": "description",
            "price": 100,
            "device_types": [
                token
            ]
        }
        res = session.post(url=f'{base_url}/{API_SERVICE}', json=payload)

        return res.json()

    request.addfinalizer(fin)
    return _service_factory


@pytest.fixture
def movie_factory(session, base_url, request):
    API_MOVIES = 'qa/movies'

    def fin():
        session.delete(url=f'{base_url}/{API_MOVIES}')

    def _movie_factory(service, session, base_url, end_date):
        """Creates movie for given service"""

        payload = {
            "id": 1,
            "name": "Blade Runner",
            "description": "Sci_fi",
            "start_date": 1577883600,
            "end_date": end_date,
            "services": [
                service['id']
            ]
        }
        res = session.post(url=f'{base_url}/{API_MOVIES}', json=payload)

        return res.json()

    request.addfinalizer(fin)
    return _movie_factory


@pytest.fixture
def time_expires():
    '''return a UNIX style timestamp - 24 hours'''
    seconds_in_a_day = 60 * 60 * 24
    return int(time.time()-seconds_in_a_day)


@pytest.fixture
def time_valid():
    '''return a UNIX style timestamp + 24 hours'''
    seconds_in_a_day = 60 * 60 * 24
    return int(time.time()+seconds_in_a_day)