
from utils.__init__ import *


class Fetcher:

    def __init__(self):
        self.PROXY_SITES = [
            'https://proxy-daily.com/',
            #'http://free-proxy.cz/en/',
            'https://free-proxy-list.net/',
            'http://nntime.com/proxy-list-02.htm',
            'https://www.sslproxies.org/'
        ]
        self.PATTERN = r'(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3}):(\d{1,5})'

    def fetch_proxies(self, proxies):
        for site in self.PROXY_SITES:
            try:
                res = requests.get(site)
                if res.status_code == requests.codes.ok:
                    fetched = re.findall(self.PATTERN, res.text)
                    for proxy in fetched:
                        _ = '.'.join(proxy[:len(proxy)-1]) + f':{proxy[len(proxy)-1]}'
                        proxies.append(_)
            except Exception as e:
                print(e)
        return proxies
            