
from utils.__init__ import *
from __init__ import *
import time


def check_proxy(address, port, table_widget, row):
    try:
        requests.get(
            'http://www.163.com',
            headers=HEADERS
        )
        result = QTableWidgetItem('good')
        result.setForeground(QBrush(QColor(0, 255, 0)))
    except ConnectionError:
        result = QTableWidgetItem('bad')
        result.setForeground(QBrush(QColor(255, 0, 0)))
    finally:
        time.sleep(0.1)
        table_widget.setItem(row, 3, result)

