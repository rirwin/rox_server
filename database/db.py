
try:
    from database.rocksdb_database import RocksDB
    db = RocksDB()
except:
    import mock
    db = mock.Mock()
