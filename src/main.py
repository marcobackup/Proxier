
from __init__ import *
from table import *


ui, _ = loadUiType('mainwindow.ui')

class Proxier(QMainWindow, ui):

    def __init__(self, parent=None):
        super(Proxier, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.threadpool = QThreadPool()
        self.init_UI()
        # starting handling...
        self.buttons_handler()

    """
        starting app...
    """
    def init_UI(self):
        #model = ProxiesTable([['fwjiofw', 'wmi23o', '323', '2no3ig3oi4'], ['nn2ironio32r', 'r23nrj2390r', 'j23if2', '23fi32']], ['Address', 'Port', 'Country', 'Status'], self)
        self.tableWidget.horizontalHeader().hide()
        self.tableWidget.verticalHeader().hide()
        tool_bar = QToolBar('menuBar')

    """
        buttons handler
    """
    def buttons_handler(self):
        self.fetch_proxies = FetchProxies()
        self.fetch_proxies.proxyChanged.connect(self.on_proxy_changed)
        self.fetch_proxies.start()

    def on_proxy_changed(self, value):
        proxy = value.split(':')
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)
        self.tableWidget.setItem(row, 0, QTableWidgetItem(proxy[0]))
        self.tableWidget.setItem(row, 1, QTableWidgetItem(proxy[1]))
        self.tableWidget.setItem(row, 2, QTableWidgetItem('fewiofweio'))
        self.tableWidget.setItem(row, 3, QTableWidgetItem('checking...'))
        threading.Thread(target=check_proxy, args=(proxy[0], proxy[1], self.tableWidget, row),).start()
        #self.check_proxies = CheckProxies(proxy[0], proxy[1], row)
        #self.check_proxies.statusChanged.connect(self.on_proxy_status_changed)
        #self.check_proxies.start()

    def on_proxy_status_changed(self, value):
        status = value
        print(status['status'], status['row'])


    
def main():
    app = QApplication([])
    window = Proxier()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()

