from proxier.utils import *
from proxier import *


reader = geoip.Reader('proxier/utils/GeoIP.mmdb')


class Http:

    def __init__(self, site: str, address: str, port: str):
        """ Initialize Http class

        Args:
            site (str): checker site
            address (str): proxy address
            port (str): proxy port
        """
        self.site     = site
        self.address  = address
        self.port     = port
        self.response = {}

    def http_config(self) -> dict:
        """ Get HTTP proxy configuration

        Returns:
            dict: HTTP proxy configuration
        """
        return {
            'http': f'http://{self.address}:{self.port}',
            'https': f'https://{self.address}:{self.port}'
        }

    def socks4_config(self) -> dict:
        """ Get Socks4 configuration

        Returns:
            dict: Socks4 configuration
        """
        return {
            'http': f'socks4://{self.address}:{self.port}',
            'https': f'socks4://{self.address}:{self.port}'
        }

    def socks5_config(self) -> dict:
        """ Get Socks5 configuration

        Returns:
            dict: Socks5 configuration
        """
        return {
            'http': f'socks5://{self.address}:{self.port}',
            'https': f'socks5://{self.address}:{self.port}'
        }

    def request(self, proxy_config: dict) -> dict:
        """ HTTP request with proxy configuration

        Args:
            proxy_config (dict): proxy configuration to use

        Returns:
            dict: result
        """
        try:
            t1 = time.time()
            res = requests.head(
                self.site,
                headers=HEADERS,
                timeout=TIMEOUT,
                proxies=proxy_config
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


def check_proxy(site: str, address: str, port: str) -> dict:
    """ Check proxy and return result

    Args:
        site (str): checker site
        address (str): proxy address
        port (str): proxy port

    Returns:
        dict: result
    """
    http = Http(site, address, port)
    resp = http.request(http.http_config())

    if resp['status']:
        resp['type'] = 'http'
    else:
        resp = http.request(http.socks4_config())

        if resp['status']:
            resp['type'] = 'socks4'
        else:
            resp = http.request(http.socks5_config())

            if resp['status']:
                resp['type'] = 'socks5'
            else:
                resp['type'] = None

    return resp
