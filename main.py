import requests
import queue
from fake_useragent import UserAgent


class Request():

    def get(self, link, headers=None):
        if headers is None:
            r = requests.get(link)
        else:
            r = requests.get(link, headers=headers)
        return r

    def post(self, link, payload, headers=None):
        # format for payload:
        # {"type": "json/data", "payload": {"key1": "val1", "key2", "val2"}}
        if headers is None:
            if payload['type'] == 'json':
                r = requests.get(link, json=payload['payload'])
            elif payload['type'] == 'data':
                r = requests.get(link, data=payload['payload'])
            else:
                raise Exception("Payload type is invalid")
        else:
            if payload['type'] == 'json':
                r = requests.get(link, headers=headers, json=payload['payload'])
            elif payload['type'] == 'data':
                r = requests.get(link, headers=headers, data=payload['payload'])
            else:
                raise Exception("Payload type is invalid")

        return r

    def delete(self, link, headers=None):
        if headers is None:
            r = requests.get(link)
        else:
            r = requests.get(link, headers=headers)
        return r

    def put(self, link, headers=None):
        if headers is None:
            r = requests.get(link)
        else:
            r = requests.get(link, headers=headers)
        return r


class Response:
    def __init__(self, resp_request):
        self.headers = resp_request.headers
        self.cookies = resp_request.cookies
        self.content = resp_request.content
        self.text = resp_request.text
        self.json = resp_request.json()
        self.info = {"status_code": resp_request.status_code, "reason": resp_request.reason}


class Session:
    def __init__(self, proxy_settings=None, user_agent="random", cookies=None):
        # proxy_settings format:
        # {"proxy": "username:password@ip:port", "proxy_type": "socks5/https"}
        # cookies format:
        # {"key1": "val1", "key2": "val2"}
        self.session = requests.Session()
        self.proxy_setting = proxy_settings
        if user_agent == "random":
            ua = UserAgent()
            self.user_agent = ua.random
        else:
            self.user_agent = user_agent
        if cookies is not None:
            self.session.cookies.update(cookies)

        self.session.headers.update({"user-agent": self.user_agent})

    def get(self, link, headers=None):
        resp = Request().get(link, headers=headers)
        return Response(resp)

    def post(self):
        pass

    def delete(self):
        pass

    def put(self):
        pass
