from fastRQ import Session, Queue
import threading

# sess = Session()
# r = sess.get('https://google.com')
# print(r.info)

def x(payload):
    print(payload)

q1 = Queue(callback=x)

for i in range(5):
    q1.put(i)

print(q1.getQueue())