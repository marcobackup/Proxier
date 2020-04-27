
from __init__ import *


class CheckProxies(QThread):

    statusChanged = pyqtSignal(dict)

    def __init__(self, proxies, parent=None):
        QThread.__init__(self, parent)
        self.proxies = proxies

    def run(self):
        for proxy in self.proxies:
            status = check_proxy(proxy['address'], proxy['port'])
            self.statusChanged.emit({'status': status, 'row': proxy['row']})


class FetchProxies(QThread):
    
    proxyChanged = pyqtSignal(dict)
    fetcher = Fetcher()

    def run(self):
        sites = self.fetcher.get_proxies_sites()
        for site in sites:
            proxy = self.fetcher.fetch_proxy(site)
            for _ in proxy:
                #time.sleep(0.01)
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
        #self.proxyChanged.emit({
        #    ''
        #})
