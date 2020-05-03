
from utils.__init__ import *
from __init__ import *
import time, geoip2.database as geoip


reader = geoip.Reader('utils/GeoIP.mmdb')





class Http:

    def __init__(self, site, address, port):
        self.site = site
        self.address = address
        self.port = port
        self.response = {}

    def http_config(self):
        return {
            'http': f'http://{self.address}:{self.port}',
            'https': f'https://{self.address}:{self.port}'
        }

    def socks4_config(self):
        return {
            'http': f'socks4://{self.address}:{self.port}',
            'https': f'socks4://{self.address}:{self.port}'
        }

    def socks5_config(self):
        return {
            'http': f'socks5://{self.address}:{self.port}',
            'https': f'socks5://{self.address}:{self.port}'
        }

    def request(self, proxies_config):
        try:
            t1 = time.time()
            res = requests.head(
                self.site,
                headers=HEADERS,
                timeout=TIMEOUT,
                proxies=proxies_config
            )
            t2 = time.time()
            if res.status_code == 200:
                try:
                    city = reader.city(self.address).registered_country.names['en']
                except:
                    city = None
                self.response = {
                    'address': self.address,
                    'port': self.port,
                    'status': True,
                    'city': city,
                    'ms': str(round((t2-t1)*1000))
                }
            else:
                self.response = {
                    'address': self.address,
                    'port': self.port,
                    'status': False,
                    'city': None,
                    'ms': None
                }
        except:
            self.response = {
                'address': self.address,
                'port': self.port,
                'status': False,
                'city': None,
                'ms': None
            }  
        finally:
            return self.response


def check_proxy(site, address, port):
    http = Http(site, address, port)
    resp = http.request(http.http_config())
    if resp['status']:
        resp['type'] = 'http'
        return resp
    else:
        resp = http.request(http.socks4_config())
        if resp['status']:
            resp['type'] = 'socks4'
            return resp
        else:
            resp = http.request(http.socks5_config())
            if resp['status']:
                resp['type'] = 'socks5'
                return resp
            else:
                resp['type'] = None
                return resp

