
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
    
    proxyChanged = pyqtSignal(str)
    fetcher = Fetcher()

    def run(self):
        proxies = self.fetcher.fetch_proxies()
        for proxy in proxies:
            #time.sleep(0.01)
            self.proxyChanged.emit(proxy)
        self.proxyChanged.emit('stop')
