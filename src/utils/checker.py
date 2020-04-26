
from utils.__init__ import *
from __init__ import *
import time


def check_proxy(address, port):
    try:
        requests.get(
            'http://www.163.com',
            headers=HEADERS
        )
        return True
    except ConnectionError:
        return False


