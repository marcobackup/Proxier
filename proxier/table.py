
from __init__ import *


class CheckProxies(QThread):

    statusChanged = pyqtSignal(dict)

    def __init__(self, proxies, parent=None):
        QThread.__init__(self, parent)
        self.proxies = proxies
        self.pool = Pool(150)

    def run(self):
        futures = []
        for proxy in self.proxies:
            address, port = proxy.split(':')
            futures.append({
                'future': self.pool.apply_async(check_proxy, ['http://www.163.com', address, port]),
                'address': address,
                'port': port
            })
        for future in futures:
            self.statusChanged.emit({
                'status': future['future'].get(), 
                'address': future['address'], 
                'port': future['port']
            })


class FetchProxies(QThread):
    
    proxyChanged = pyqtSignal(dict)
    fetcher = Fetcher()

    def run(self):
        sites = self.fetcher.get_proxies_sites()
        for site in sites:
            proxy = self.fetcher.fetch_proxy(site)
            for _ in proxy:
                if _:
                    self.proxyChanged.emit(
                        {
                            'status': True,
                            'work': True,
                            'proxy': _,
                            'source': site 
                        }
                    )
                else:
                    self.proxyChanged.emit(
                        {
                            'status': False
                        }
                    )
        self.proxyChanged.emit(
            {
                'status': True,
                'work': False
            }
        )
