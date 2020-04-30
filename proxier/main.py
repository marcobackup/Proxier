from __init__ import *
from table import *

ui, _ = loadUiType('gui/mainwindow.ui')

class Proxier(QMainWindow, ui):

    def __init__(self, parent=None):
        super(Proxier, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.init_UI()
        self.proxies_leecher = []
        self.proxies_checker = []
        # starting handling...
        self.buttons_handler()

    """
        starting app...
    """
    def init_UI(self):
        self.proxies_fetch_table.horizontalHeader().hide()
        self.proxies_fetch_table.verticalHeader().hide()
        self.proxies_checker_table.horizontalHeader().hide()
        self.proxies_checker_table.verticalHeader().hide()
        self.proxies_checker_table.setIconSize(QSize(20, 20))


    """
        buttons handler
    """
    def buttons_handler(self):
        self.bitbucket_btn.clicked.connect(self.open_bitbucket_repo)
        self.start_fetch_btn.clicked.connect(self.fetch_proxies)
        self.save_fetch_btn.clicked.connect(self.save_hits)
        self.clear_fetch_btn.clicked.connect(self.clear_fetch_table)
        self.addlist_checker_btn.clicked.connect(self.show_import_menu)
        self.save_checker_btn.clicked.connect(self.show_save_menu)
        self.start_checker_btn.clicked.connect(self.start_checker)

    def open_bitbucket_repo(self):
        webbrowser.open('https://bitbucket.org/Marklavoro/proxier')

    def clear_fetch_table(self):
        self.proxies_fetch_table.clear()
        self.proxies_fetch_table.setRowCount(0)
        self.proxies_leecher = []
        self.source_fetch_lbl.setText(
            '<span style=" font-weight:600; color:#ffffff;">Cleared!</span>'
        )      
        self.hits_fetch_lbl.setText(f'<span style=" font-weight:600; color:#2cff21;">0</span>')
        self.errors_fetch_lbl.setText(f'<span style=" font-weight:600; color:#ff3c0b;">0</span>')

    def show_import_menu(self):
        import_menu = QMenu(self)
        import_menu.setStyleSheet('QMenu { background-color: rgb(66, 69, 74); color: white; } QMenu::item:selected { background: white; color: rgb(66, 69, 74); } QMenu[hide="true"]::right-arrow { }')
        import_menu.addAction('Import from leecher', self.import_proxies_fetched)
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

    def import_proxies_fetched(self):
        for address, port in self.get_hits():
            proxy = f'{address}:{port}'
            if proxy not in self.proxies_checker:
                self.proxies_checker.append(proxy)
                hits = self.proxies_checker_lbl.text().split('">')[1].split('</')[0]
                self.proxies_checker_lbl.setText(f'<span style=" font-size:10pt; font-weight:600; color:#ffffff;">{int(hits) + 1}</span>')

    def save_hits(self):
        file_name = QFileDialog.getSaveFileName(self, 'Proxier - Save Hits')
        if file_name[0] != '':
            with open(file_name[0], 'w') as file_:
                for address, port in self.get_hits():
                    file_.write(f'{address}:{port}\n')
                file_.close()
                self.source_fetch_lbl.setText(f'<span style=" font-weight:600; color:#ffffff;">Exported {len(self.proxies_leecher)} hits!</span>')
        
    def fetch_proxies(self):
        proxy_sites = []
        for site in self.link_fetch_text.toPlainText().split('\n'):
            if site != '': proxy_sites.append(site)
        btn_status = self.start_fetch_btn.text()
        self.fetch_proxies = FetchProxies(proxy_sites)
        self.fetch_proxies.proxyChanged.connect(self.on_proxy_changed)
        if 'START' in btn_status:
            self.clear_fetch_table()
            self.start_fetch_btn.setText('STOP')
            self.fetch_proxies.start()
        else:
            self.start_fetch_btn.setText('START')

    def start_checker(self):
        btn_status = self.start_checker_btn.text()
        self.check_proxies = CheckProxies(self.proxies_checker, self.site_checker_line.text(), self)
        self.check_proxies.statusChanged.connect(self.on_proxy_checked)
        if 'START' in btn_status:
            self.start_checker_btn.setText('STOP')
            self.check_proxies.start()
        else:
            self.start_checker_btn.setText('START')

    def on_proxy_changed(self, value):
        status = value['status']
        if not status:
            errors = self.errors_fetch_lbl.text().split('">')[1].split('</')[0]
            self.errors_fetch_lbl.setText(f'<span style=" font-weight:600; color:#ff3c0b;">{int(errors) + 1}</span>')
        else:
            if value['work']:
                proxy = value['proxy'].split(':')
                if value['proxy'] not in self.proxies_leecher:
                    self.proxies_leecher.append(value['proxy'])
                    row = self.proxies_fetch_table.rowCount()
                    self.proxies_fetch_table.insertRow(row)
                    self.proxies_fetch_table.setItem(row, 0, QTableWidgetItem(proxy[0]))
                    self.proxies_fetch_table.setItem(row, 1, QTableWidgetItem(proxy[1]))
                    self.proxies_fetch_table.setItem(row, 2, QTableWidgetItem(value['source']))
                    hits = self.hits_fetch_lbl.text().split('">')[1].split('</')[0]
                    self.hits_fetch_lbl.setText(f'<span style=" font-weight:600; color:#2cff21;">{int(hits) + 1}</span>')
                    self.source_fetch_lbl.setText('<span style=" font-weight:600; color:#ffffff;">{}</span>'.format(value['source']))
            else:
                self.source_fetch_lbl.setText(f'<span style=" font-weight:600; color:#ffffff;">Leeched {len(self.proxies_leecher)} proxies!</span>')
                self.start_fetch_btn.setText('START')

    def on_proxy_checked(self, value):
        if value['status']:
            row = self.proxies_checker_table.rowCount()
            self.proxies_checker_table.insertRow(row)
            self.proxies_checker_table.setItem(row, 0, QTableWidgetItem(value['address']))
            self.proxies_checker_table.setItem(row, 1, QTableWidgetItem(value['port']))
            import resource_rc
            item = QTableWidgetItem()
            item.setSizeHint(QSize(20, 20))
            city = str(value['city']).replace(' ', '-')
            item.setIcon(QIcon(f'assets/ico/{city}-Flag.ico'))
            self.proxies_checker_table.setItem(row, 2, item)
            self.proxies_checker_table.setItem(row, 3, QTableWidgetItem(value['ms'] + 'ms'))
            hits = self.hits_checker_lbl.text().split('">')[1].split('</')[0]
            self.hits_checker_lbl.setText(f'<span style="font-size:10pt; font-weight:600; color:#2cff21;">{int(hits) + 1}</span>')            
        else:
            bad = self.bad_checker_lbl.text().split('">')[1].split('</')[0]
            self.bad_checker_lbl.setText(f'<span style="font-size:10pt; font-weight:600; color:#ff3c0b;">{int(bad) + 1}</span>')
        checked = self.checked_checker_lbl.text().split('">')[1].split('</')[0]
        self.checked_checker_lbl.setText(f'<span style="font-size:10pt; font-weight:600; color:#ffffff;">{int(checked) + 1}</span>')
        proxies = self.proxies_checker_lbl.text().split('">')[1].split('</')[0]
        self.proxies_checker_lbl.setText(f'<span style="font-size:10pt; font-weight:600; color:#ffffff;">{int(proxies) - 1}</span>')



def main():
    app = QApplication([])
    window = Proxier()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()


