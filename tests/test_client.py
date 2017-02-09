import mock
import simplejson
import pytest

from client.http_client import JSON_HEADERS
from client.http_client import RoxHttpClient


class TestClient(object):

    @pytest.fixture
    def client(self):
        return RoxHttpClient()

    @pytest.yield_fixture
    def patch_conn(self, client):
        with mock.patch.object(client, 'conn') as patched_conn:
            yield patched_conn

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
    def test_set_calls_set_endpoint_properly(self, patch_conn, client, key, value):
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

    def test_set_bulk_calls_set_endpoint_properly(self, patch_conn, client):
        data = {'key_{}'.format(i): 'value_{}'.format(i) for i in range(10)}
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

    def test_set_cached_calls_set_bulk_endpoint_after_limit(self, patch_conn, client):
        data = [('key_{}'.format(i), 'value_{}'.format(i)) for i in range(10)]
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

    def test_add_calls_add_endpoint_properly(self, patch_conn, client):
        row_key = 'row_key_0'
        data = {'key_0': 'value_0', 'key_1': 'value_1'}
        client.add(row_key, data)
        expected_call_args = [
            mock.call(
                'POST',
                '/add',
                simplejson.dumps({row_key: data}),
                JSON_HEADERS
            )
        ]
        assert patch_conn.request.call_args_list == expected_call_args

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

    def test_clear_calls_clear_endpoint_properly(self, patch_conn, client):
        key = 'key1'
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

    def test_clear_bulk_calls_clear_endpoint_properly(self, patch_conn, client):
        keys = ['key1', 'key2']
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
