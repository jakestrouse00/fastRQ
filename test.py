from fastRQ import Session, Queue
import threading

import asyncio


# sess = Session()
# r = sess.get('https://google.com')
# print(r.info)


def pp(var):
    print(var)
x = Queue(callback=pp, timeout=0)
# x.start()
x.put("10m")

for i in range(5):
    jj = input("?? ")
    x.put(jj)

print(x.get_queue())
x.start()