
from utils.__init__ import *


class Fetcher:

    def __init__(self):
        self.PROXY_SITES = [
            'https://proxy-daily.com/',
            #'http://free-proxy.cz/en/',
            'https://free-proxy-list.net/',
            'http://nntime.com/proxy-list-02.htm',
            'https://www.sslproxies.org/',
            'http://proxy.ipcn.org/proxylist2.html',
            'http://best-proxy.ru/feed',
            'http://www.proxylists.net/?HTTP',
            'http://ab57.ru/downloads/proxyold.txt',
            'http://www.freeproxy.ru/download/lists/goodproxy.txt',
            'http://www.proxylists.net/http_highanon.txt',
            'http://www.atomintersoft.com/high_anonymity_elite_proxy_list',
            'http://www.atomintersoft.com/transparent_proxy_list',
            'http://www.atomintersoft.com/anonymous_proxy_list'
        ]
        self.PATTERN = r'(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3}):(\d{1,5})'

    def worker(self, site, result):
        res = requests.get(
            site,
            headers=HEADERS
        )
        if res.status_code == requests.codes.ok:
            result.append(res.text)

    def fetch_proxies(self):
        proxies = []
        for site in self.PROXY_SITES:
            try:
                res = []
                th = threading.Thread(target=self.worker, args=(site, res,))
                th.start()
                th.join()
                for _ in res:
                    fetched = re.findall(self.PATTERN, _)
                    for proxy in fetched:
                        _ = '.'.join(proxy[:len(proxy)-1]) + f':{proxy[len(proxy)-1]}'
                        proxies.append(_)
            except:
                pass
        return proxies    

        