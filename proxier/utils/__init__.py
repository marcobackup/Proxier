from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool
from requests.exceptions import *
import requests
import re
import threading
import os
import zipfile
import socket
import struct
import time
import geoip2.database as geoip


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0'
}
TIMEOUT = 7
