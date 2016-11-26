import mock
from simplejson import dumps
import pytest
from urllib.parse import quote

from rox_client.http_client import assert_key_is_hashable
from rox_client.http_client import KeyIsNotHashableException
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
                    '/set?key={}&value={}'.format(quote(dumps(key)), quote(dumps(value)))
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
        mock_response.read = mock.Mock(return_value=dumps(value))
        mock_conn.getresponse = mock.Mock(return_value=mock_response)
        with mock.patch.object(client, 'conn', mock_conn) as patch_conn:
            returned_value = client.get(key)
            expected_call_args = [
                mock.call(
                    'GET',
                    '/get?key={}'.format(quote(dumps(key)))
                )
            ]
            patch_conn.request.call_args_list == expected_call_args
            assert returned_value == value

    @pytest.mark.parametrize(
        'key, exception',
        [
            ('1.2.3.4', None),
            ({'a': 'b'}, KeyIsNotHashableException),
            (['a', 'b', 'c'], KeyIsNotHashableException),
        ]
    )
    def test_key_must_be_serializable_check(self, key, exception):

        @assert_key_is_hashable
        def do_nothing(key):
            pass

        if exception:
            with pytest.raises(exception):
                do_nothing(key)
        else:
            do_nothing(key)
