
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

    """
        buttons handler
    """
    def buttons_handler(self):
        self.bitbucket_btn.clicked.connect(self.open_bitbucket_repo)
        self.start_fetch_btn.clicked.connect(self.fetch_proxies)
        self.save_fetch_btn.clicked.connect(self.save_hits)
        self.addlist_checker_btn.clicked.connect(self.show_import_menu)
        self.save_checker_btn.clicked.connect(self.show_save_menu)

    def open_bitbucket_repo(self):
        webbrowser.open('https://bitbucket.org/Marklavoro/proxier')

    def show_import_menu(self):
        import_menu = QMenu(self)
        import_menu.setStyleSheet('QMenu { background-color: rgb(66, 69, 74); color: white; } QMenu::item:selected { background: white; color: rgb(66, 69, 74); } QMenu[hide="true"]::right-arrow { }')
        import_menu.addAction('Import from leecher')
        import_menu.addAction('Import from folder')
        self.addlist_checker_btn.setMenu(import_menu)

    def show_save_menu(self):
        save_menu = QMenu(self)
        save_menu.setStyleSheet('QMenu { background-color: rgb(66, 69, 74); color: white; } QMenu::item:selected { background: white; color: rgb(66, 69, 74); } QMenu[hide="true"]::right-arrow { }')
        save_menu.addAction('Save all')
        sub_menu = save_menu.addMenu('Save by type')
        sub_menu.addAction('http/s')
        sub_menu.addAction('socks4')
        sub_menu.addAction('socks5')
        save_menu.addAction('Save by country')
        self.save_checker_btn.setMenu(save_menu)

    def get_hits(self):
        rows_count = self.proxies_fetch_table.rowCount()
        for row in range(rows_count):
            address = self.proxies_fetch_table.item(row, 0).text()
            port = self.proxies_fetch_table.item(row, 1).text()
            yield address, port

    def save_hits(self):
        file_name = QFileDialog.getSaveFileName(self, 'Proxier - Save Hits')
        if file_name != '':
            with open(file_name[0], 'w') as file_:
                for address, port in self.get_hits():
                    file_.write(f'{address}:{port}\n')
                file_.close()
        
    def fetch_proxies(self):
        btn_status = self.start_fetch_btn.text()
        self.fetch_proxies = FetchProxies()
        self.fetch_proxies.proxyChanged.connect(self.on_proxy_changed)
        if 'START' in btn_status:
            self.start_fetch_btn.setText('STOP')
            self.fetch_proxies.start()
        else:
            self.start_fetch_btn.setText('START')
            #self.fetch_proxies.signalsBlocked()

    def on_proxy_changed(self, value):
        status = value['status']
        if not status:
            errors = self.errors_fetch_lbl.text().split('">')[1].split('</')[0]
            self.errors_fetch_lbl.setText(f'<span style=" font-weight:600; color:#ff3c0b;">{int(errors) + 1}</span>')
        else:
            if value['work']:
                proxy = value['proxy'].split(':')
                if proxy[0] not in self.proxies:
                    self.proxies.append(proxy)
                    row = self.proxies_fetch_table.rowCount()
                    self.proxies_fetch_table.insertRow(row)
                    self.proxies_fetch_table.setItem(row, 0, QTableWidgetItem(proxy[0]))
                    self.proxies_fetch_table.setItem(row, 1, QTableWidgetItem(proxy[1]))
                    self.proxies_fetch_table.setItem(row, 2, QTableWidgetItem(value['source']))
                    hits = self.hits_fetch_lbl.text().split('">')[1].split('</')[0]
                    self.hits_fetch_lbl.setText(f'<span style=" font-weight:600; color:#2cff21;">{int(hits) + 1}</span>')
                    self.source_fetch_lbl.setText('<span style=" font-weight:600; color:#ffffff;">{}</span>'.format(value['source']))
            else:
                self.proxies = []
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


