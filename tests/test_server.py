import pytest

from rox_server.server import app
from rox_server.server import db


app.testing = True


class TestServerRouteBehavior(object):

    @pytest.fixture
    def client(self):
        return app.test_client()

    def test_home_gets_instructions(self, client):
        response = client.get('/')
        assert response.status_code == 200
        assert b'Welcome to KV server.' in response.get_data()

    def test_set_places_object_in_db(self, client):
        response = client.get('set?key=5&value=2')
        assert response.status_code == 200
        assert db.get(b'5') == b'2'

    def test_set_key_with_no_value_returns_bad_request(self, client):
        response = client.get('set?key=5')
        assert response.status_code == 400

    def test_get_retrieves_object_from_db(self, client):
        db.put(b'5', b'1')
        response = client.get('get?key=5')
        assert response.status_code == 200
        assert db.get(b'5') == b'1'

    def test_get_with_no_key_returns_bad_request(self, client):
        response = client.get('get?')
        assert response.status_code == 400

    def test_get_with_no_value_in_db_returns_not_found(self, client):
        response = client.get('get?key=123456')
        assert response.status_code == 404
