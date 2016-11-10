import mock
import pytest
from servers import string_dict_kv_store


class TestStringDictKVStore(object):

    key = 'midtown'
    value = 'doornail'

    @pytest.yield_fixture
    def patch_db(self):
        mock_db = {}
        with mock.patch('servers.string_dict_kv_store.db', mock_db):
            yield

    @pytest.fixture
    def store(self, patch_db):
        return string_dict_kv_store

    def test_index_returns_string_with_200(self, store):
        result, status_code = store.index()
        assert isinstance(result, str)
        assert status_code == 200

    @pytest.mark.parametrize(
        'args, expected_db, expected_response, expected_response_code',
        [
           ({'key': key, 'value': value}, {key: value}, string_dict_kv_store.OK, 200),
           ({'missing param': key}, {}, string_dict_kv_store.BAD_REQUEST, 400),
        ]
    )
    def test_set_behavior(self, args, expected_db, expected_response, expected_response_code, store):
        mock_request = mock.Mock()
        mock_request.args = args
        with mock.patch('servers.string_dict_kv_store.request', mock_request):
            response, status_code = string_dict_kv_store.set()
            assert string_dict_kv_store.db == expected_db
            assert response == expected_response
            assert status_code == expected_response_code

    @pytest.mark.parametrize(
        'args, input_db, expected_response, expected_response_code',
        [
           ({'key': key}, {key: value},  value, 200),
           ({'missing param': key}, {key: value}, string_dict_kv_store.BAD_REQUEST, 400),
           ({'key': 'key not in db'}, {key: value}, string_dict_kv_store.KEY_NOT_FOUND, 404),
        ]
    )
    def test_get_behavior(self, args, input_db, expected_response, expected_response_code, store):
        mock_request = mock.Mock()
        mock_request.args = args
        store.db = input_db
        with mock.patch('servers.string_dict_kv_store.request', mock_request):
            response, status_code = string_dict_kv_store.get()
            assert response == expected_response
            assert status_code == expected_response_code
