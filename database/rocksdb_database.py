import itertools
import rocksdb


class RocksDB(object):

    _db = None

    def __init__(self):
        self._db = rocksdb.DB("rox_server_kernel.db", rocksdb.Options(create_if_missing=True))  # pragma: no cover

    def add_to_row(self, row, data):  # make sure no key already there?
        batch = rocksdb.WriteBatch()
        for key, value in data.items():
            batch.put(str.encode(row + '.' + key), str.encode(value))
        self._db.write(batch)

    def get_row(self, keys):
        it = self._db.iteritems()
        data = {}
        for key in keys:
            prefix = str.encode(key)
            it.seek(prefix)
            row = dict(itertools.takewhile(lambda item: item[0].startswith(prefix), it))
            row_data = {k[len(prefix) + 1:].decode(): v.decode() for k, v in row.items()}
            data.update({key: row_data})
        return data

    def set(self, data):
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
