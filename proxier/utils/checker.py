
from utils.__init__ import *
from __init__ import *
import time


def check_proxy(site, address, port):
    try:
        proxies = {
            'http': f'http://{address}:{port}',
            'https': f'https://{address}:{port}'
        }
        requests.get(
            site,
            headers=HEADERS,
            timeout=TIMEOUT,
            proxies=proxies
        )
        return True
    except:
        return False


