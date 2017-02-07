from database.rocksdb_database import RocksDB
db = RocksDB()
db.add_to_row('1.2.3.4', {'a': '1', 'b': '2'})
print(db.get_row(['1.2.3.4']))

db.put({'key': 'value'})
print(db.get(['key']))
