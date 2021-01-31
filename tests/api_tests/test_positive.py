import requests
import pytest


class TestPositive:
    def test_add_booking(self, add_new_booking, booking_data):
        r = add_new_booking
        assert r['booking'] == booking_data

    def test_add_booking_with_special_chars(self, api_address, booking_special_characters):
        r = requests.post(api_address, json=booking_special_characters).json()
        assert r['booking'] == booking_special_characters

    def test_get_single_booking(self, add_new_booking, api_address, booking_data):
        id = add_new_booking['bookingid']
        r = requests.get(api_address + f"/{id}")
        assert booking_data == r.json()

    def test_get_all_bookings(self, add_new_booking, api_address, booking_data):
        id = add_new_booking['bookingid']
        r = requests.get(api_address)
        assert r.status_code == 200
        assert len(r.json()) >= 1

    def test_update_booking(self, add_new_booking, api_address, booking_data, token):
        id = add_new_booking['bookingid']
        modified_data = booking_data.copy()
        modified_data['firstname'] = "tmp_user_firstname_upd"
        modified_data['lastname'] = "tmp_user_lastname_upd"
        modified_data['totalprice'] = 20000
        modified_data['depositpaid'] = True
        modified_data['additionalneeds'] = ""

        r = requests.put(api_address + f"/{id}", json=modified_data, headers={'Cookie': f'token={token}'})
        assert r.status_code == 200
        assert modified_data == r.json()

    @pytest.mark.parametrize("modified_data",
                             [
                                 ({"firstname": "tmp_user_firstname"}),
                                 ({"lastname": "tmp_user_lastname"}),
                                 ({"totalprice": 10000}),
                                 ({"depositpaid": False}),
                                 ({"additionalneeds": "Breakfast"})
                             ])
    def test_partial_update_booking(self, add_new_booking, api_address, token, modified_data):
        r = add_new_booking
        id = r['bookingid']
        r = requests.patch(api_address + f"/{id}", json=modified_data, headers={'Cookie': f'token={token}'})
        assert r.status_code == 200
        for k in modified_data.keys():
            assert modified_data[k] == r.json()[k]

    def test_remove_booking(self, add_new_booking, api_address, booking_data, token):
        id = add_new_booking['bookingid']
        r_del = requests.delete(api_address + f"/{id}", headers={'Cookie': f'token={token}'})
        assert r_del.status_code == 201
        r_get_by_id = requests.get(api_address + f"/{id}")
        assert r_get_by_id.status_code == 404