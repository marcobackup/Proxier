import requests, re, threading, os, zipfile, socket, struct
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool
from requests.exceptions import *


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0'
}
TIMEOUT = 7
