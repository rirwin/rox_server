class DictDatabase(object):

    _db = {}

    def put(self, key, value):
        self._db[key] = value

    def get(self, key):
        return self._db[key]
