try:
    import rocksdb
    db = rocksdb.DB("rox_server_kernel.db", rocksdb.Options(create_if_missing=True))  # pragma: no cover
    print("Using RocksDB")                                                            # pragma: no cover
except ImportError:
    from database.dict_database import DictDatabase
    db = DictDatabase()
    print("Using In-Memory Dictionary")
