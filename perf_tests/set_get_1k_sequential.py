from rox_client.http_client import RoxHttpClient

import time


c = RoxHttpClient()

# hack to set host to docker's host
c.conn.host = '192.168.99.100'

t0 = time.time()

for i in range(1000):
    c.set(str(i), str(i))

t1 = time.time()

for i in range(1000):
    c.get(str(i))

t2 = time.time()

print("{0} seconds for set, \n{1} seconds for get, and \n{2} total".format(t1-t0, t2-t1, t2-t0))
