
from __init__ import *
from table import *


ui, _ = loadUiType('gui/mainwindow.ui')

class Proxier(QMainWindow, ui):

    def __init__(self, parent=None):
        super(Proxier, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.init_UI()
        self.proxies = []
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
        self.startbtn.clicked.connect(self.fetch_proxies)

    def fetch_proxies(self):
        self.proxies = []
        self.fetch_proxies = FetchProxies()
        self.fetch_proxies.proxyChanged.connect(self.on_proxy_changed)
        self.fetch_proxies.start()

    def on_proxy_changed(self, value):
        if value == 'stop':
            self.check_proxies = CheckProxies(self.proxies)
            self.check_proxies.statusChanged.connect(self.on_proxy_status_changed)
            self.check_proxies.start()
            self.proxies = []
        else:
            proxy = value.split(':')
            row = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row)
            self.tableWidget.setItem(row, 0, QTableWidgetItem(proxy[0]))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(proxy[1]))
            self.tableWidget.setItem(row, 2, QTableWidgetItem('fewiofweio'))
            self.tableWidget.setItem(row, 3, QTableWidgetItem('checking...'))
            self.proxies.append({
                'address': proxy[0],
                'port': proxy[1],
                'row': row
            })

    def on_proxy_status_changed(self, value):
        result = None
        if value['status']:
            result = QTableWidgetItem('good')
            result.setForeground(QBrush(QColor(0, 255, 0)))
        else:
            result = QTableWidgetItem('bad')
            result.setForeground(QBrush(QColor(255, 0, 0)))
        time.sleep(0.1)
        self.tableWidget.setItem(value['row'], 3, result)

    
def main():
    app = QApplication([])
    window = Proxier()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()

