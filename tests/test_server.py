import mock
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
        data = {'5': '1', 'a': 'b'}
        with mock.patch.object(db, 'get', return_value=data):
            response = client.get('get', data=simplejson.dumps(['5', 'a']), content_type='application/json')
            assert response.status_code == 200
            assert response.data == simplejson.dumps(data).encode()

    def test_get_with_no_key_returns_bad_request(self, client):
        response = client.get('get?')
        assert response.status_code == 400

    def test_get_with_no_value_in_db_returns_empty_dict(self, client):
        with mock.patch.object(db, 'get', return_value={}):
            response = client.get('get', data=simplejson.dumps(['abcd']), content_type='application/json')
            assert response.data == b'{}'

    def test_set_calls_put_to_db(self, client):
        data = {'key_0': 'value_0', 'key_1': 'value_1'}
        with mock.patch.object(db, 'put') as patch_put:
            response = client.get('set', data=simplejson.dumps(data), content_type='application/json')
            assert response.status_code == 200
            assert patch_put.call_args_list == [mock.call(data)]

    def test_set_not_json_returns_bad_request(self, client):
        response = client.get('set?blah')
        assert response.status_code == 400

    def test_clear_calls_delete_in_db(self, client):
        keys = ['key_1', 'key_5']
        with mock.patch.object(db, 'delete') as patch_delete:
            response = client.get('clear', data=simplejson.dumps(keys), content_type='application/json')
            assert response.status_code == 200
            assert patch_delete.call_args_list == [mock.call(keys)]

    def test_clear_with_no_key_returns_bad_request(self, client):
        response = client.get('clear?')
        assert response.status_code == 400
