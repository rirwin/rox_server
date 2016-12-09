import rocksdb


class RocksDB(object):

    _db = None

    def __init__(self):
        self._db = rocksdb.DB("rox_server_kernel.db", rocksdb.Options(create_if_missing=True))  # pragma: no cover

    def put(self, key, value):
        self._db.put(str.encode(key), str.encode(value))

    def get(self, key):
        value = self._db.get(str.encode(key))
        if value:
            return value.decode()

    def delete(self, key):
        self._db.delete(str.encode(key))
