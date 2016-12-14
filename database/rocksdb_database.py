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

    def get(self, keys):
        data = self._db.multi_get([str.encode(key) for key in keys])
        if data:
            return {k.decode(): v.decode() for k, v in data.items() if v is not None}

    def delete(self, keys):
        batch = rocksdb.WriteBatch()
        for key in keys:
            batch.delete(str.encode(key))
        self._db.write(batch)

    def print_all_contents(self):
        it = self._db.iteritems()
        it.seek_to_first()
        print(list(it))
