import pytest
import simplejson

from server.http_server import app
from server.http_server import db


app.testing = True


class TestServerRouteBehavior(object):

    @pytest.fixture
    def client(self):
        return app.test_client()

    def test_home_gets_instructions(self, client):
        response = client.get('/')
        assert response.status_code == 200
        assert b'Welcome to KV server.' in response.get_data()

    def test_get_retrieves_object_from_db(self, client):
        db.put(b'5', b'1')
        response = client.get('get', data=simplejson.dumps('5'), content_type='application/json')
        assert response.status_code == 200
        assert db.get(b'5') == b'1'

    def test_get_with_no_key_returns_bad_request(self, client):
        response = client.get('get?')
        assert response.status_code == 400

    def test_get_with_no_value_in_db_returns_not_found(self, client):
        response = client.get('get', data=simplejson.dumps('abcd'), content_type='application/json')
        assert response.status_code == 404

    def test_set_places_object_in_db_as_byte_string(self, client):
        data = {'key_0': 'value_0'}
        response = client.get('set', data=simplejson.dumps(data), content_type='application/json')
        assert response.status_code == 200
        assert db.get(str.encode('key_0')) == str.encode('value_0')

    def test_set_bulk_places_all_objects_in_db_as_byte_strings(self, client):
        data = {'key_%d' % i: 'value_%d' % i for i in range(10)}
        response = client.get('set', data=simplejson.dumps(data), content_type='application/json')
        assert response.status_code == 200
        for k, v in data.items():
            assert db.get(str.encode(k)) == str.encode(v)

    def test_set_not_json_returns_bad_request(self, client):
        response = client.get('set?blah')
        assert response.status_code == 400

    def test_clear_clears_keys_in_db(self, client):
        db.put(b'5', b'1')
        db.put(b'7', b'2')
        response = client.get('clear', data=simplejson.dumps([b'5', b'7']), content_type='application/json')
        assert response.status_code == 200
        assert db.get(b'5') is None
        assert db.get(b'7') is None

    def test_clear_with_no_key_returns_bad_request(self, client):
        response = client.get('clear?')
        assert response.status_code == 400
