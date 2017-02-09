import itertools
import rocksdb


class RocksDB(object):

    _db = None

    def __init__(self):
        self._db = rocksdb.DB("rox_server_kernel.db", rocksdb.Options(create_if_missing=True))  # pragma: no cover

    def add(self, data):
        batch = rocksdb.WriteBatch()
        for row, row_data in data.items():
            for key, value in row_data.items():
                batch.put(str.encode(row + '.' + key), str.encode(value))
        self._db.write(batch)

    def get_rows(self, rows):
        it = self._db.iteritems()
        data = {}
        for row in rows:
            print(row)
            prefix = str.encode(row)
            it.seek(prefix)
            prefix_data = dict(itertools.takewhile(lambda item: item[0].startswith(prefix), it))
            row_data = {k[len(prefix) + 1:].decode(): v.decode() for k, v in prefix_data.items()}
            data.update({row: row_data})
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
