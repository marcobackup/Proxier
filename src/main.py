
from __init__ import *


fetcher = Fetcher()
ui, _ = loadUiType('mainwindow.ui')

class Proxier(QMainWindow, ui):

    def __init__(self, parent=None):
        super(Proxier, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
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
        self.startbtn.clicked.connect(self.fetch_proxies)

    def fetch_proxies(self):
        row = self.tableWidget.rowCount()
        proxies = []
        th = threading.Thread(target=fetcher.fetch_proxies, args=(proxies,))
        th.start()
        th.join()
        for proxy in proxies:
            self.tableWidget.insertRow(row)
            self.tableWidget.setItem(row, 0, QTableWidgetItem(proxy))
            self.tableWidget.setItem(row, 1, QTableWidgetItem('fewniofwe'))
            self.tableWidget.setItem(row, 2, QTableWidgetItem('fewiofweio'))
            self.tableWidget.setItem(row, 3, QTableWidgetItem('checking...'))

    
def main():
    app = QApplication([])
    window = Proxier()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()

