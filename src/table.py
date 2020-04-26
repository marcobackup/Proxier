
from __init__ import *


class CheckProxies(QThread):

    statusChanged = pyqtSignal(dict)

    def __init__(self, address, port, row, parent=None):
        QThread.__init__(self, parent)
        self.address = address
        self.port    = port
        self.row     = row

    def run(self):
        status = check_proxy(self.address, self.port)
        time.sleep(0.1)
        self.statusChanged.emit({'status': status, 'row': self.row})


class FetchProxies(QThread):
    
    proxyChanged = pyqtSignal(str)
    fetcher = Fetcher()

    def run(self):
        proxies = self.fetcher.fetch_proxies()
        for proxy in proxies:
            time.sleep(0.01)
            self.proxyChanged.emit(proxy)

