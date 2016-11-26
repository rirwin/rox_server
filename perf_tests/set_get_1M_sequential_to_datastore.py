import time

import rocksdb

from rox_server.dict_database import DictDatabase

dbr = rocksdb.DB("rox_server_kernel_perf.db", rocksdb.Options(create_if_missing=True))

NUM_ITER = 1000000

t0 = time.time()

for i in range(NUM_ITER):
    dbr.put(str.encode(str(i)), str.encode(str(i)))

t1 = time.time()

for i in range(NUM_ITER):
    dbr.get(str.encode(str(i)))

t2 = time.time()

print("Python in-memory dict")
print("{0} seconds for set, \n{1} seconds for get, and \n{2} seconds total".format(t1-t0, t2-t1, t2-t0))


dbp = DictDatabase()

t0 = time.time()

for i in range(NUM_ITER):
    dbp.put(str.encode(str(i)), str.encode(str(i)))

t1 = time.time()

for i in range(NUM_ITER):
    dbp.get(str.encode(str(i)))

t2 = time.time()

print("RocksDB")
print("{0} seconds for set, \n{1} seconds for get, and \n{2} seconds total".format(t1-t0, t2-t1, t2-t0))
