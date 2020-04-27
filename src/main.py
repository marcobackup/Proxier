
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
        self.proxies_fetch_table.horizontalHeader().hide()
        self.proxies_fetch_table.verticalHeader().hide()
        #tool_bar = QToolBar('menuBar')

    """
        buttons handler
    """
    def buttons_handler(self):
        self.start_fetch_btn.clicked.connect(self.fetch_proxies)

    def fetch_proxies(self):
        self.proxies = []
        self.fetch_proxies = FetchProxies()
        self.fetch_proxies.proxyChanged.connect(self.on_proxy_changed)
        self.start_fetch_btn.setText('STOP')
        self.fetch_proxies.start()

    def on_proxy_changed(self, value):
        status = value['status']
        if not status:
            errors = self.errors_fetch_lbl.text().split('">')[1].split('</')[0]
            self.errors_fetch_lbl.setText(f'<span style=" font-weight:600; color:#ff3c0b;">{int(errors) + 1}</span>')
        else:
            if value['work']:
                proxy = value['proxy'].split(':')
                row = self.proxies_fetch_table.rowCount()
                self.proxies_fetch_table.insertRow(row)
                self.proxies_fetch_table.setItem(row, 0, QTableWidgetItem(proxy[0]))
                self.proxies_fetch_table.setItem(row, 1, QTableWidgetItem(proxy[1]))
                self.proxies_fetch_table.setItem(row, 2, QTableWidgetItem(value['source']))
                hits = self.hits_fetch_lbl.text().split('">')[1].split('</')[0]
                self.hits_fetch_lbl.setText(f'<span style=" font-weight:600; color:#2cff21;">{int(hits) + 1}</span>')
                self.source_fetch_lbl.setText('<span style=" font-weight:600; color:#ffffff;">{}</span>'.format(value['source']))
            else:
                self.source_fetch_lbl.setText('<span style=" font-weight:600; color:#ffffff;">Finished!</span>')
                self.start_fetch_btn.setText('START')

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

