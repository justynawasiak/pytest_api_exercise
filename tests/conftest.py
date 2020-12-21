import pytest
import requests


@pytest.fixture()
def api_address():
    return 'https://restful-booker.herokuapp.com/booking'


@pytest.fixture()
def booking_data():
    return \
        {
            "firstname": "tmp_user_firstname",
            "lastname": "tmp_user_lastname",
            "totalprice": 10000,
            "depositpaid": False,
            "bookingdates": {
                "checkin": "2021-01-01",
                "checkout": "2021-12-01"
            },
            "additionalneeds": "Breakfast"
        }


@pytest.fixture()
def booking_invalid_data():
    return \
        {
            "firstname": 123,
            "lastname": 123,
            "totalprice": "abc",
            "depositpaid": 1223,
            "bookingdates": {
                "checkin": "20212",
                "checkout": "20212"
            },
            "additionalneeds": 123
        }


@pytest.fixture()
def token():
    auth_data = {
        "username": "admin",
        "password": "password123"
    }
    token_r = requests.post("https://restful-booker.herokuapp.com/auth", data=auth_data)
    yield token_r.json()["token"]


@pytest.fixture()
def add_new_booking(api_address, booking_data):
    r = requests.post(api_address, json=booking_data)
    assert r.status_code == 200
    yield r.json()