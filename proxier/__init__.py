
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType

from utils.fetcher import *
from utils.checker import *
try:
    from win10toast import ToastNotifier
except:
    pass

import webbrowser
import resource_rc

