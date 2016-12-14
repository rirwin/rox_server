from client.http_client import RoxHttpClient


client = RoxHttpClient(host='192.168.99.100', port=5000, cache_size_limit=8)

# Clears keys from previous run if exists
keys = ['key{}'.format(i) for i in range(1, 25)]
for k in keys:
    client.clear(k)

client.set('key1', 'value1')
assert client.get('key1') == {'key1': 'value1'}


data = {'key{}'.format(i): 'value{}'.format(i) for i in range(1, 10)}
client.set_bulk(data)
for k, v in data.items():
    assert client.get(k) == {k: v}


data = {'key{}'.format(i): 'value{}'.format(i) for i in range(10, 18)}
for k, v in data.items():
    client.set_cached(k, v)

assert client._cache == {}

data_part_2 = {'key{}'.format(i): 'value{}'.format(i) for i in range(18, 25)}
for k, v in data_part_2.items():
    client.set_cached(k, v)

for k, v in data.items():
    assert client.get(k) == {k: v}

for k in data_part_2.keys():
    assert client.get(k) == {}

client.flush()

for k, v in data_part_2.items():
    assert client.get(k) == {k: v}


assert client.get_bulk(list(data_part_2.keys())) == data_part_2
