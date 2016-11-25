import rocksdb


class RocksDBDatabase(object):

    _db = rocksdb.DB("rox_server_kernel.db", rocksdb.Options(create_if_missing=True))

    def put(self, key, value):
        self._db.put(key, value)

    def get(self, key):
        return self._db.get(key)
