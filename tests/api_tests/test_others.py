import requests


class TestOthers:

    def test_health_check(self, api_address):
        r = requests.get('https://restful-booker.herokuapp.com/ping')
        assert r.status_code == 201




