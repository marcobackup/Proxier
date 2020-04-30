
from utils.__init__ import *
from __init__ import *
import time, geoip2.database as geoip


reader = geoip.Reader('utils/GeoIP.mmdb')

def check_proxy(site, address, port):
    response = {}
    try:
        proxies = {
            'http': f'socks5://{address}:{port}',
            'https': f'socks5://{address}:{port}'
        }
        t1 = time.time()
        requests.get(
            site,
            headers=HEADERS,
            timeout=TIMEOUT,
            proxies=proxies
        )
        t2 = time.time()
        try:
            city = reader.city(address).registered_country.names['en']
        except:
            city = None
        response = {
            'address': address,
            'port': port,
            'status': True,
            'city': city,
            'ms': str(round((t2-t1)*1000))
        }
    except:
        response = {
            'address': address,
            'port': port,
            'status': False,
            'city': None,
            'ms': None
        }
    finally:
        return response


