import requests
import queue
import time
from fake_useragent import UserAgent
import threading


class Queue:
    def __init__(self, callback, timeout=None, threadedCallback=False):
        """
        Currently does not work because for the life of me I cannot figure out how to pass a callback function.
        """
        self.timeout = timeout
        self.threadedCallback = threadedCallback
        self.callbackFunc = callback
        self.queue = queue.Queue()
        threading.Thread(target=self.watchQueue).start()

    def watchQueue(self):
        while True:
            if not self.queue.empty:
                print(55)
                item = self.queue.get()
                if self.threadedCallback:
                    threading.Thread(target=self.callbackFunc, args=(item,)).start()
                else:
                    self.callbackFunc(item)
            else:
                if self.timeout is not None:
                    time.sleep(self.timeout)

    def getQueue(self):
        return list(self.queue.queue)

    def put(self, item):
        self.queue.put(item)


class Request():
    def __init__(self, session):
        self.sess = session.session
        self.session = session

    def get(self, link, headers=None):
        if self.session.proxy_setting is not None:
            if self.session.proxy_setting['proxy_type'] == 'socks5':
                proxy = dict(http=f"socks5://{self.session.proxy_setting['proxy_type']}",
                             https=f"socks5://{self.session.proxy_setting['proxy_type']}")
            elif self.session.proxy_setting['proxy_type'] == 'https':
                proxy = dict(http=f"http://{self.session.proxy_setting['proxy_type']}",
                             https=f"https://{self.session.proxy_setting['proxy_type']}")
            else:
                raise Exception("Invalid proxy_type")
            r = self.sess.get(link, headers=headers, proxies=proxy)
        else:
            r = self.sess.get(link, headers=headers)
        return r

    def post(self, link, payload, headers=None):
        # format for payload:
        # {"type": "json/data", "payload": {"key1": "val1", "key2", "val2"}}
        if self.session.proxy_setting is not None:
            if self.session.proxy_setting['proxy_type'] == 'socks5':
                proxy = dict(http=f"socks5://{self.session.proxy_setting['proxy_type']}",
                             https=f"socks5://{self.session.proxy_setting['proxy_type']}")
            elif self.session.proxy_setting['proxy_type'] == 'https':
                proxy = dict(http=f"http://{self.session.proxy_setting['proxy_type']}",
                             https=f"https://{self.session.proxy_setting['proxy_type']}")
            else:
                raise Exception("Invalid proxy_type")
        if payload['type'] == 'json':
            r = self.sess.post(link, headers=headers, json=payload['payload'], proxies=proxy)
        elif payload['type'] == 'data':
            r = self.sess.post(link, headers=headers, data=payload['payload'], proxies=proxy)
        else:
            raise Exception("Payload type is invalid")

        return r

    def delete(self, link, headers=None):
        if self.session.proxy_setting is not None:
            if self.session.proxy_setting['proxy_type'] == 'socks5':
                proxy = dict(http=f"socks5://{self.session.proxy_setting['proxy_type']}",
                             https=f"socks5://{self.session.proxy_setting['proxy_type']}")
            elif self.session.proxy_setting['proxy_type'] == 'https':
                proxy = dict(http=f"http://{self.session.proxy_setting['proxy_type']}",
                             https=f"https://{self.session.proxy_setting['proxy_type']}")
            else:
                raise Exception("Invalid proxy_type")
        r = self.sess.delete(link, headers=headers, proxies=proxy)

        return r

    def put(self, link, payload, headers=None):
        if self.session.proxy_setting is not None:
            if self.session.proxy_setting['proxy_type'] == 'socks5':
                proxy = dict(http=f"socks5://{self.session.proxy_setting['proxy_type']}",
                             https=f"socks5://{self.session.proxy_setting['proxy_type']}")
            elif self.session.proxy_setting['proxy_type'] == 'https':
                proxy = dict(http=f"http://{self.session.proxy_setting['proxy_type']}",
                             https=f"https://{self.session.proxy_setting['proxy_type']}")
            else:
                raise Exception("Invalid proxy_type")
        if payload['type'] == 'json':
            r = self.sess.put(link, headers=headers, json=payload['payload'], proxies=proxy)
        elif payload['type'] == 'data':
            r = self.sess.put(link, headers=headers, data=payload['payload'], proxies=proxy)
        else:
            raise Exception("Payload type is invalid")
        return r


class Response:
    def __init__(self, resp_request):
        self.headers = resp_request.headers
        self.cookies = resp_request.cookies
        self.content = resp_request.content
        self.text = resp_request.text
        try:
            self.json = resp_request.json()
        except:
            self.json = None
        self.info = {"status_code": resp_request.status_code, "reason": resp_request.reason}


class Session:
    def __init__(self, proxy_settings=None, user_agent="default", cookies=None):
        # proxy_settings format:
        # {"proxy": "username:password@ip:port", "proxy_type": "socks5/https"}
        # cookies format:
        # {"key1": "val1", "key2": "val2"}
        self.session = requests.Session()
        self.proxy_setting = proxy_settings
        if user_agent == "random":
            ua = UserAgent()
            self.user_agent = ua.random
        elif user_agent == 'default':
            self.user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36"
        else:
            self.user_agent = user_agent
        if cookies is not None:
            self.session.cookies.update(cookies)

        self.session.headers.update({"user-agent": self.user_agent})

    def get(self, link, headers=None):
        resp = Request(self).get(link, headers=headers)
        return Response(resp)

    def post(self, link, payload, headers=None):
        resp = Request(self).post(link, headers=headers, payload=payload)
        return Response(resp)

    def delete(self, link, headers=None):
        resp = Request(self).delete(link, headers=headers)
        return Response(resp)

    def put(self, link, payload, headers=None):
        resp = Request(self).post(link, headers=headers, payload=payload)
        return Response(resp)
