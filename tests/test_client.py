import mock
import simplejson
import pytest

from client.http_client import JSON_HEADERS
from client.http_client import RoxHttpClient


class TestClient(object):

    @pytest.fixture
    def client(self):
        return RoxHttpClient()

    def test_client_init_opens_http_connection(self):
        client = RoxHttpClient(host='1.2.3.4', port=5000, cache_size_limit=50)
        assert client.conn.host == '1.2.3.4'
        assert client.conn.port == 5000
        assert client.cache_size_limit == 50

    @pytest.mark.parametrize(
        'key, value',
        [
            ('key', 'value'),
            ('1.2.3.4', {'attr1': 1, 'attr2': True, 'attr3': 0.75})
        ]
    )
    def test_set_calls_set_endpoint_properly(self, client, key, value):
        with mock.patch.object(client, 'conn') as patch_conn:
            client.set(key, value)
            expected_call_args = [
                mock.call(
                    'POST',
                    '/set',
                    simplejson.dumps({key: value}),
                    JSON_HEADERS
                )
            ]
            assert patch_conn.request.call_args_list == expected_call_args

    def test_set_bulk_calls_set_endpoint_properly(self, client):
        data = {'key_{}'.format(i): 'value_{}'.format(i) for i in range(10)}
        with mock.patch.object(client, 'conn') as patch_conn:
            client.set_bulk(data)
            expected_call_args = [
                mock.call(
                    'POST',
                    '/set',
                    simplejson.dumps(data),
                    JSON_HEADERS
                )
            ]
            assert patch_conn.request.call_args_list == expected_call_args

    def test_set_cached_calls_set_bulk_endpoint_after_limit(self, client):
        data = [('key_{}'.format(i), 'value_{}'.format(i)) for i in range(10)]
        with mock.patch.object(client, 'conn') as patch_conn:
            for k, v in data:
                client.set_cached(k, v)

            expected_call_args = [
                mock.call(
                    'POST',
                    '/set',
                    simplejson.dumps({i[0]: i[1] for i in data[:client.cache_size_limit]}),
                    JSON_HEADERS
                )
            ]
            assert patch_conn.request.call_args_list == expected_call_args
            assert client._cache == {i[0]: i[1] for i in data[client.cache_size_limit:]}

    @pytest.mark.parametrize(
        'key, value',
        [
            ('key', 'value'),
            ('1.2.3.4', {'attr1': 1, 'attr2': True, 'attr3': 0.75})
        ]
    )
    def test_get_calls_get_endpoint_properly(self, key, value, client):
        mock_conn = mock.Mock()
        mock_response = mock.Mock()
        mock_decode = mock.Mock()
        mock_decode.decode = mock.Mock(return_value=simplejson.dumps({key: value}))
        mock_response.read = mock.Mock(return_value=mock_decode)
        mock_conn.getresponse = mock.Mock(return_value=mock_response)
        with mock.patch.object(client, 'conn', mock_conn) as patch_conn:
            returned_value = client.get(key)
            expected_call_args = [
                mock.call(
                    'GET',
                    '/get',
                    simplejson.dumps([key]),
                    JSON_HEADERS
                )
            ]
            assert patch_conn.request.call_args_list == expected_call_args
            assert returned_value == {key: value}

    def test_get_bulk_get_endpoint_properly(self, client):
        data = {'a': 'b', 'c': 'd'}
        mock_conn = mock.Mock()
        mock_response = mock.Mock()
        mock_decode = mock.Mock()
        mock_decode.decode = mock.Mock(return_value=simplejson.dumps(data))
        mock_response.read = mock.Mock(return_value=mock_decode)
        mock_conn.getresponse = mock.Mock(return_value=mock_response)
        with mock.patch.object(client, 'conn', mock_conn) as patch_conn:
            returned_value = client.get_bulk(list(data.keys()))
            expected_call_args = [
                mock.call(
                    'GET',
                    '/get',
                    simplejson.dumps(list(data.keys())),
                    JSON_HEADERS
                )
            ]
            assert patch_conn.request.call_args_list == expected_call_args
            assert returned_value == data

    def test_flush_calls_set_bulk_with_cache(self, client):
        cache = {'a': 'b'}
        client._cache = cache
        with mock.patch.object(client, 'set_bulk') as patch_set_bulk:
            client.flush()
            assert patch_set_bulk.call_args_list == [mock.call(cache)]

    def test_clear_calls_clear_endpoint_properly(self, client):
        key = 'key1'
        with mock.patch.object(client, 'conn') as patch_conn:
            client.clear(key)
            expected_call_args = [
                mock.call(
                    'POST',
                    '/clear',
                    simplejson.dumps([key]),
                    JSON_HEADERS
                )
            ]
            assert patch_conn.request.call_args_list == expected_call_args

    def test_clear_bulk_calls_clear_endpoint_properly(self, client):
        keys = ['key1', 'key2']
        with mock.patch.object(client, 'conn') as patch_conn:
            client.clear_bulk(keys)
            expected_call_args = [
                mock.call(
                    'POST',
                    '/clear',
                    simplejson.dumps(keys),
                    JSON_HEADERS
                )
            ]
            assert patch_conn.request.call_args_list == expected_call_args
