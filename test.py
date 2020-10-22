from fastRQ import Session
import threading


# sess = Session()
# r = sess.get('https://google.com')
# print(r.info)

def o(j):
    print(1)
    print(j)
def x(thing):
    thing(2)

x(o)