class DictDatabase(object):
    """This class is used for when rocksdb fails to load,
    like when a machine doesn't have the rocksdb dependencies.
    Related, it's also useful for testing and running locally.
    """
    _db = {}

    def put(self, key, value):
        self._db[str.encode(key)] = str.encode(value)

    def add(self, key, sub_key, value):
        if self._db[key]:
            self._db[key].update({sub_key: value})
        else:
            self._db[key] = {sub_key: value}

    def get(self, key):
        value = self._db.get(str.encode(key))
        if value:
            return value.decode()

    def delete(self, key):
        del self._db[str.encode(key)]
