from proxier import *


checker_wait = QWaitCondition()

class CheckProxies(QThread):

    statusChanged = pyqtSignal(dict)

    def __init__(self, proxies: list, site: str, parent=None):
        """ Initialize checker thread

        Args:
            proxies (list): proxies to check
            site (str): checker url
            parent ([type], optional): [description]. Defaults to None.
        """
        super(CheckProxies, self).__init__()
        self.proxies = proxies
        self.site    = site # www.baidu.com
        self.pool    = Pool(250)
        self.mutex   = QMutex()
        self.pause   = None

    def resume(self):
        """ Resume thread
        """
        self.mutex.lock()
        self.pause = False
        self.mutex.unlock()
        checker_wait.wakeAll()

    def suspend(self):
        """ Suspend thread
        """
        self.mutex.lock()
        self.pause = True
        self.mutex.unlock()

    def run(self):
        """ Run thread
        """
        futures = []

        for proxy in self.proxies:
            try:
                address, port = proxy.split(':')
                futures.append(
                    {
                        'future': self.pool.apply_async(check_proxy, [self.site, address, port]),
                        'address': address,
                        'port': port
                    }
                )
            except:
                self.statusChanged.emit(
                    {
                        'status': 'error'
                    }
                )

        for future in futures:
            self.mutex.lock()

            # If thread is paused
            if self.pause:
                checker_wait.wait(self.mutex)

            self.mutex.unlock()
            future = future['future'].get()

            self.statusChanged.emit(
                {
                    'status': future['status'],
                    'city': future['city'],
                    'ms': future['ms'],
                    'address': future['address'],
                    'port': future['port'],
                    'type': future['type']
                }
            )

        self.statusChanged.emit(
            {
                'status': 'end',
            }
        )


fetch_wait = QWaitCondition()

class FetchProxies(QThread):

    statusChanged = pyqtSignal(dict)

    def __init__(self, proxy_sites: list, parent=None):
        """ Initialize fetcher thread

        Args:
            proxy_sites (list): site to scrape
            parent ([type], optional): [description]. Defaults to None.
        """
        super(FetchProxies, self).__init__()
        self.fetcher = Fetcher(proxy_sites)
        self.mutex   = QMutex()
        self.pause   = None

    def resume(self):
        """ Resume thread
        """
        self.mutex.lock()
        self.pause = False
        self.mutex.unlock()
        fetch_wait.wakeAll()

    def suspend(self):
        """ Suspend thread
        """
        self.mutex.lock()
        self.pause = True
        self.mutex.unlock()

    def run(self):
        """ Run thread
        """
        sites = self.fetcher.get_proxies_sites()

        for site in sites:
            proxy = self.fetcher.fetch_proxy(site)

            for _ in proxy:
                self.mutex.lock()

                if self.pause:
                    fetch_wait.wait(self.mutex)
                self.mutex.unlock()

                if _:
                    self.statusChanged.emit(
                        {
                            'status': True,
                            'work': True,
                            'proxy': _,
                            'source': site
                        }
                    )
                else:
                    self.statusChanged.emit(
                        {
                            'status': False
                        }
                    )

        self.statusChanged.emit(
            {
                'status': True,
                'work': False
            }
        )

