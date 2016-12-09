try:
    from database.rocksdb_database import RocksDB
    db = RocksDB()
    print("Using RocksDB")
except ImportError:
    from database.dict_database import DictDatabase
    db = DictDatabase()
    print("Using In-Memory Dictionary")
