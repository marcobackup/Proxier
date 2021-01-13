from proxier import *
from proxier.table import (
    CheckProxies, 
    FetchProxies
)


ui, _ = loadUiType('proxier/gui/mainwindow.ui')

class Proxier(QMainWindow, ui):

    def __init__(self, parent=None):
        super(Proxier, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.init_UI()
        self.proxies_leecher = []
        self.proxies_checker = {'list': [], 'countries': {}, 'types': {}}
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
        self.github_btn.clicked.connect(self.open_github_repo)
        self.start_fetch_btn.clicked.connect(self.fetch_proxies)
        self.save_fetch_btn.clicked.connect(self.save_hits)
        self.clear_fetch_btn.clicked.connect(self.clear_fetch_table)
        self.addlist_checker_btn.clicked.connect(self.show_import_menu)
        self.save_checker_btn.clicked.connect(self.show_save_menu)
        self.start_checker_btn.clicked.connect(self.start_checker)
        # LEECHER THREAD
        proxy_sites = []
        for site in self.link_fetch_text.toPlainText().split('\n'):
            if site != '': proxy_sites.append(site)
        self.fetch_proxies = FetchProxies(proxy_sites, self)
        self.fetch_proxies.statusChanged.connect(self.on_proxy_fetched)
        # CHECKER THREAD
        self.check_proxies = CheckProxies(self.proxies_checker['list'], self.site_checker_line.text(), self)
        self.check_proxies.statusChanged.connect(self.on_proxy_checked)

    def open_github_repo(self):
        webbrowser.open('https://github.com/Marklab9/proxier')

    def clear_fetch_table(self):
        clear_ok = QMessageBox.question(self, 'Clear all', 'Are you sure?', QMessageBox.Yes | QMessageBox.No)
        if clear_ok == QMessageBox.Yes:
            self.proxies_fetch_table.clear()
            self.proxies_fetch_table.setRowCount(0)
            self.proxies_leecher = []
            self.source_fetch_lbl.setText(
                '<span style=" font-weight:600; color:#ffffff;">Cleared!</span>'
            )      
            self.hits_fetch_lbl.setText('<span style=" font-weight:600; color:#2cff21;">0</span>')
            self.errors_fetch_lbl.setText('<span style=" font-weight:600; color:#ff3c0b;">0</span>')

    def clear_checker_table(self):
        clear_ok = QMessageBox.question(self, 'Clear all', 'Are you sure?', QMessageBox.Yes | QMessageBox.No)
        if clear_ok == QMessageBox.Yes:
            self.proxies_checker_table.clear()
            self.proxies_checker_table.setRowCount(0)
            self.proxies_checker = []
            self.source_checker_lbl.setText(
                '<span style=" font-weight:600; color:#ffffff;">Cleared!</span>'
            )      
            self.hits_checker_lbl.setText('<span style=" font-weight:600; color:#2cff21;">0</span>')
            self.errors_checker_lbl.setText('<span style=" font-weight:600; color:#ff3c0b;">0</span>')
            self.checked_checker_lbl.setText('<span style=" font-size:10pt; font-weight:600; color:#ffffff;">0</span>')
            self.bad_checker_lbl.setText('<span style=" font-weight:600; color:#ff3c0b;">0</span>')
            self.proxies_checker_lbl.setText('<span style=" font-weight:600; color:#ffffff;">0</span>')

    def show_import_menu(self):
        import_menu = QMenu(self)
        import_menu.setStyleSheet('QMenu { background-color: rgb(66, 69, 74); color: white; } QMenu::item:selected { background: white; color: rgb(66, 69, 74); } QMenu[hide="true"]::right-arrow { }')
        import_menu.addAction('Import from leecher', self.import_proxies_fetched)
        import_menu.addAction('Import from folder', self.import_proxies_file)
        self.addlist_checker_btn.setMenu(import_menu)

    def show_save_menu(self):
        save_menu = QMenu(self)
        save_menu.setStyleSheet('QMenu { background-color: rgb(66, 69, 74); color: white; } QMenu::item:selected { background: white; color: rgb(66, 69, 74); } QMenu[hide="true"]::right-arrow { }')
        save_menu.addAction('Save all', self.save_all)
        sub_menu = save_menu.addMenu('Save by type')
        sub_menu.addAction('http/s', self.save_http)
        sub_menu.addAction('socks4', self.save_socks4)
        sub_menu.addAction('socks5', self.save_socks5)
        save_menu.addAction('Save by country', self.save_by_country)
        self.save_checker_btn.setMenu(save_menu)

    def save_http(self):
        file_name = QFileDialog.getSaveFileName(self, f'Proxier - Save Http/s')
        if file_name[0] != '':
            with open(file_name[0], 'w') as file_:
                for type_ in self.proxies_checker['types']:
                    if type_ == 'http':
                        for hit in self.proxies_checker['types'][type_]:
                            file_.write(f'{hit}\n')
                file_.close()

    def save_socks4(self):
        file_name = QFileDialog.getSaveFileName(self, f'Proxier - Save Http/s')
        if file_name[0] != '':
            with open(file_name[0], 'w') as file_:
                for type_ in self.proxies_checker['types']:
                    if type_ == 'socks4':
                        for hit in self.proxies_checker['types'][type_]:
                            file_.write(f'{hit}\n')
                file_.close()

    def save_socks5(self):
        file_name = QFileDialog.getSaveFileName(self, f'Proxier - Save Http/s')
        if file_name[0] != '':
            with open(file_name[0], 'w') as file_:
                for type_ in self.proxies_checker['types']:
                    if type_ == 'socks5':
                        for hit in self.proxies_checker['types'][type_]:
                            file_.write(f'{hit}\n')
                file_.close()

    def save_by_country(self):
        countries = []
        for country in self.proxies_checker['countries']:
            countries.append(country)
        country, is_pressed = QInputDialog.getItem(self, 'Proxier - Get Country', 'Country: ', countries, 0, False)
        if is_pressed and country:
            file_name = QFileDialog.getSaveFileName(self, f'Proxier - Save Hits {country}')
            if file_name[0] != '':
                with open(file_name[0], 'w') as file_:
                    for hit in self.proxies_checker['countries'][country]:
                        file_.write(f'{hit}\n')
                    file_.close()

    def save_all(self):
        file_name = QFileDialog.getSaveFileName(self, f'Proxier - Save Hits')
        if file_name[0] != '':
            with open(file_name[0], 'w') as file_:
                for country in self.proxies_checker['countries']:
                    for hit in self.proxies_checker['countries'][country]:
                        file_.write(f'{hit}\n')
                for type_ in self.proxies_checker['types']:
                    for hit in self.proxies_checker['types'][type_]:
                        file_.write(f'{hit}\n')
                file_.close()

    def get_hits(self):
        rows_count = self.proxies_fetch_table.rowCount()
        for row in range(rows_count):
            address = self.proxies_fetch_table.item(row, 0).text()
            port = self.proxies_fetch_table.item(row, 1).text()
            yield address, port

    def import_proxies_fetched(self):
        for address, port in self.get_hits():
            proxy = f'{address}:{port}'
            if proxy not in self.proxies_checker['list']:
                self.proxies_checker['list'].append(proxy)
                hits = self.proxies_checker_lbl.text().split('">')[1].split('</')[0]
                self.proxies_checker_lbl.setText(f'<span style=" font-size:10pt; font-weight:600; color:#ffffff;">{int(hits) + 1}</span>')

    def import_proxies_file(self):
        file_name = QFileDialog.getOpenFileName(self, 'Proxier - Import List')
        if file_name[0] != '':
            with open(file_name[0], 'r') as file_:
                lines = file_.readlines()
                for proxy in lines:
                    proxy = proxy.replace('\n', '')
                    if proxy not in self.proxies_checker['list']:
                        self.proxies_checker['list'].append(proxy)
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
        btn_status = self.start_fetch_btn.text()
        if 'START' in btn_status:
            self.fetch_proxies.start()
            self.clear_fetch_btn.setDisabled(True)
            self.start_fetch_btn.setText('STOP')
        elif 'RESUME' in btn_status:
            self.fetch_proxies.resume()
            self.clear_fetch_btn.setDisabled(True)
            self.start_fetch_btn.setText('STOP')
        else:
            self.clear_fetch_btn.setDisabled(False)
            self.source_fetch_lbl.setText('<span style=" font-weight:600; color:#ffffff;">Stopped.</span>')
            self.fetch_proxies.suspend()
            self.start_fetch_btn.setText('RESUME')

    def start_checker(self):
        btn_status = self.start_checker_btn.text()
        if 'START' in btn_status:
            self.start_checker_btn.setText('STOP')
            self.clear_checker_btn.setDisabled(True)
            self.addlist_checker_btn.setDisabled(True)
            self.source_checker_lbl.setText('<span style=" font-weight:600; color:#ffffff;">Checking...</span>')
            self.check_proxies.start()
        elif 'RESUME' in btn_status:
            self.check_proxies.resume()
            self.clear_checker_btn.setDisabled(True)
            self.addlist_checker_btn.setDisabled(True)
            self.source_checker_lbl.setText('<span style=" font-weight:600; color:#ffffff;">Checking...</span>')
        else:
            self.clear_checker_btn.setDisabled(False)
            self.addlist_checker_btn.setDisabled(False)
            self.source_checker_lbl.setText('<span style=" font-weight:600; color:#ffffff;">Stopped</span>')
            self.check_proxies.suspend()
            self.start_checker_btn.setText('RESUME')

    def on_proxy_fetched(self, value):
        status = value['status']
        if not status:
            errors = self.errors_fetch_lbl.text().split('">')[1].split('</')[0]
            self.errors_fetch_lbl.setText(f'<span style=" font-weight:600; color:#ff3c0b;">{int(errors) + 1}</span>')
        else:
            if value['work']:
                self.source_fetch_lbl.setText('<span style=" font-weight:600; color:#ffffff;">{}</span>'.format(value['source']))
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
            else:
                self.source_fetch_lbl.setText(f'<span style=" font-weight:600; color:#ffffff;">Leeched {len(self.proxies_leecher)} proxies!</span>')
                self.clear_fetch_btn.setDisabled(False)
                self.start_fetch_btn.setText('START')
                #try:
                #    self.toast.show_toast('Proxier', f'Leeched {len(self.proxies_leecher)} proxies!', duration=2, icon_path='assets/favicon.ico', threaded=True)
                #except:
                #    pass

    def on_proxy_checked(self, value):
        if value['status']:
            if value['status'] == 'error':
                errors = self.errors_checker_lbl.text().split('">')[1].split('</')[0]
                self.errors_checker_lbl.setText(f'<span style="font-size:10pt; font-weight:600; color:#ff3c0b;">{int(errors) + 1}</span>')                    
            elif value['status'] == 'end':
                self.start_checker_btn.setText('START')
                #try:
                #    self.toast.show_toast('Proxier', f'Proxies checked!', duration=10, icon_path='assets/favicon.ico', threaded=True)
                #except:
                #    pass
                self.source_checker_lbl.setText('<span style=" font-weight:600; color:#ffffff;">Finished</span>')
                self.clear_checker_btn.setDisabled(False)
                self.addlist_checker_btn.setDisabled(False)
            else:
                row = self.proxies_checker_table.rowCount()
                self.proxies_checker_table.insertRow(row)
                self.proxies_checker_table.setItem(row, 0, QTableWidgetItem(value['address']))
                self.proxies_checker_table.setItem(row, 1, QTableWidgetItem(value['port']))
                item = QTableWidgetItem(value['type'])
                item.setSizeHint(QSize(0, 0))
                city = str(value['city']).replace(' ', '-')
                if city not in self.proxies_checker['countries']: 
                    self.proxies_checker['countries'][city] = []
                self.proxies_checker['countries'][city].append('{}:{}'.format(value['address'], value['port']))
                type_ = value['type']
                if type_ not in self.proxies_checker['types']:
                    self.proxies_checker['types'][type_] = []
                self.proxies_checker['types'][type_].append('{}:{}'.format(value['address'], value['port']))
                item.setIcon(QIcon(f'assets/ico/{city}-Flag.ico'))
                self.proxies_checker_table.setItem(row, 2, item)
                self.proxies_checker_table.setItem(row, 3, QTableWidgetItem(value['ms'] + 'ms'))
                hits = self.hits_checker_lbl.text().split('">')[1].split('</')[0]
                self.hits_checker_lbl.setText(f'<span style="font-size:10pt; font-weight:600; color:#2cff21;">{int(hits) + 1}</span>')            
        else:
            bad = self.bad_checker_lbl.text().split('">')[1].split('</')[0]
            self.bad_checker_lbl.setText(f'<span style="font-size:10pt; font-weight:600; color:#ff3c0b;">{int(bad) + 1}</span>')
        if value['status'] != 'end':
            checked = self.checked_checker_lbl.text().split('">')[1].split('</')[0]
            self.checked_checker_lbl.setText(f'<span style="font-size:10pt; font-weight:600; color:#ffffff;">{int(checked) + 1}</span>')
            proxies = self.proxies_checker_lbl.text().split('">')[1].split('</')[0]
            self.proxies_checker_lbl.setText(f'<span style="font-size:10pt; font-weight:600; color:#ffffff;">{int(proxies) - 1}</span>')



def main():
    app = QApplication([])
    window = Proxier()
    window.show()
    app.exec_()

