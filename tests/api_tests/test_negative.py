import requests


class TestNegative:

    def test_add_booking_invalid_data(self, api_address, booking_invalid_data):
        r = requests.post(api_address, json=booking_invalid_data)
        assert r.status_code == 500

    def test_get_booking_invalid_id(self, api_address):
        r = requests.get(api_address + f"/abcdef")
        assert r.status_code == 404

    def test_update_booking_invalid_token(self, add_new_booking, api_address, booking_data):
        id = add_new_booking['bookingid']
        modified_data = booking_data.copy()
        modified_data['totalprice'] = 20000
        r = requests.put(api_address + f"/{id}", json=modified_data, headers={'Cookie': f'token=abc'})
        assert r.status_code == 403
        r_get_by_id = requests.get(api_address + f"/{id}")
        assert booking_data == r_get_by_id.json()

    def test_remove_non_existing_booking(self, api_address, token):
        r_del = requests.delete(api_address + f"/abc", headers={'Cookie': f'token={token}'})
        assert r_del.status_code == 405

    def test_remove_booking_without_token(self, add_new_booking, api_address, booking_data):
        id = add_new_booking['bookingid']
        r_del = requests.delete(api_address + f"/{id}", headers={'Cookie': f'token=abc'})
        assert r_del.status_code == 403
        r_get_by_id = requests.get(api_address + f"/{id}")
        assert r_get_by_id.status_code == 200