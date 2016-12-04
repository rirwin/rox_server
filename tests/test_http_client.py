import mock
import simplejson
import pytest

from rox_client.http_client import JSON_HEADERS
from rox_client.http_client import RoxHttpClient


class TestClient(object):

    def test_client_init_opens_http_connection(self):
        client = RoxHttpClient()
        assert client.conn.host == '0.0.0.0'
        assert client.conn.port == 5000

    @pytest.mark.parametrize(
        'key, value',
        [
            ('key', 'value'),
            ('1.2.3.4', {'attr1': 1, 'attr2': True, 'attr3': 0.75})
        ]
    )
    def test_set_calls_request_set_endpoint_properly(self, key, value):
        client = RoxHttpClient()
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
            patch_conn.request.call_args_list == expected_call_args

    @pytest.mark.parametrize(
        'key, value',
        [
            ('key', 'value'),
            ('1.2.3.4', {'attr1': 1, 'attr2': True, 'attr3': 0.75})
        ]
    )
    def test_get_calls_request_get_endpoint_properly(self, key, value):
        client = RoxHttpClient()
        mock_conn = mock.Mock()
        mock_response = mock.Mock()
        mock_decode = mock.Mock()
        mock_decode.decode = mock.Mock(return_value=value)
        mock_response.read = mock.Mock(return_value=mock_decode)
        mock_conn.getresponse = mock.Mock(return_value=mock_response)
        with mock.patch.object(client, 'conn', mock_conn) as patch_conn:
            returned_value = client.get(key)
            expected_call_args = [
                mock.call(
                    'GET',
                    '/get',
                    simplejson.dumps(key),
                    JSON_HEADERS
                )
            ]
            patch_conn.request.call_args_list == expected_call_args
            assert returned_value == value

    def test_set_bulk_calls_request_set_endpoint_properly(self):
        client = RoxHttpClient()
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
            patch_conn.request.call_args_list == expected_call_args

