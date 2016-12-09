import rocksdb


class RocksDB(object):

    _db = None

    def __init__(self):
        self._db = rocksdb.DB("rox_server_kernel.db", rocksdb.Options(create_if_missing=True))  # pragma: no cover

    def put(self, data):
        batch = rocksdb.WriteBatch()
        for key, value in data.items():
            batch.put(str.encode(key), str.encode(value))
        self._db.write(batch)

    def get(self, key):
        value = self._db.get(str.encode(key))
        if value:
            return value.decode()

    def delete(self, keys):
        batch = rocksdb.WriteBatch()
        for key in keys:
            batch.delete(str.encode(key))
        self._db.write(batch)

    def print_all_contents(self):
        it = self._db.iteritems()
        it.seek_to_first()
        print(list(it))
