import mock
import pytest
from servers import bytes_rocksdb_kv_store


class TestBytesRocksDBKVStore(object):

    key = 'midtown'
    value = 'doornail'

    def test_index_returns_string_with_200(self):
        result, status_code = bytes_rocksdb_kv_store.index()
        assert isinstance(result, str)
        assert status_code == 200

    @pytest.mark.parametrize(
        'request_args, expected_set_args, expected_response, expected_response_code',
        [
           ({'key': key, 'value': value}, (key, value), bytes_rocksdb_kv_store.OK, 200),
           ({'missing param': key}, None, bytes_rocksdb_kv_store.BAD_REQUEST, 400),
        ]
    )
    def test_set_behavior(self, request_args, expected_set_args, expected_response, expected_response_code):
        mock_request = mock.Mock()
        mock_request.args = request_args
        mock_db = mock.Mock()
        mock_db.put = mock.Mock()
        with \
                mock.patch('servers.bytes_rocksdb_kv_store.request', mock_request), \
                mock.patch('servers.bytes_rocksdb_kv_store.db', mock_db):

            response, status_code = bytes_rocksdb_kv_store.set()
            if mock_db.put.call_args:
                assert mock_db.put.call_args == mock.call(*expected_set_args)
            assert response == expected_response
            assert status_code == expected_response_code

    @pytest.mark.parametrize(
        'request_args, get_ret_value, expected_response, expected_response_code',
        [
           ({'key': key}, value, value, 200),
           ({'missing param': key}, None, bytes_rocksdb_kv_store.BAD_REQUEST, 400),
           ({'key': 'key not in db'}, None, bytes_rocksdb_kv_store.KEY_NOT_FOUND, 404),
        ]
    )
    def test_get_behavior(self, request_args, get_ret_value, expected_response, expected_response_code):
        mock_request = mock.Mock()
        mock_request.args = request_args
        mock_db = mock.Mock()
        mock_db.get = mock.Mock(return_value=get_ret_value)
        with \
                mock.patch('servers.bytes_rocksdb_kv_store.request', mock_request), \
                mock.patch('servers.bytes_rocksdb_kv_store.db', mock_db):
            response, status_code = bytes_rocksdb_kv_store.get()
            assert response == expected_response
            assert status_code == expected_response_code
