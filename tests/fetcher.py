
import requests, random, re, threading, time
from bs4 import BeautifulSoup
from geoip import geolite2


def get_random_site():
    SITES = [
        'https://proxy-daily.com/',
        'http://free-proxy.cz/en/',
        'https://free-proxy-list.net/',
        'http://nntime.com/proxy-list-02.htm',
        'https://www.sslproxies.org/'
    ]
    return random.choice(SITES)

def check_proxy(proxy):
    proxies = {
        'http': f'http://{proxy}',
        'https': f'http://{proxy}'
    }
    try:
        print(f'{proxy} checking...')
        b = time.time()
        requests.get(
            'http://www.google.com',
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'},
            proxies=proxies
        )
        a = time.time()
        e = round(((a - b) * 1000))
        try:
            print(proxy.split(':')[0])
            match = geolite2.lookup()
            if match is None: match = None
            else: match = match.country
            print(f'{proxy} LIVE {e}ms - {match}')
        except Exception as e:
            print(e)
    except Exception:
        pass

def fetch_proxies(url):
    res = requests.get(
        url
    )
    body = BeautifulSoup(res.text, 'html.parser')
    proxies = body.find('div', {'class': 'freeProxyStyle'})
    for _ in proxies:
        for proxy in _.split('\n'):
            threading.Thread(target=check_proxy, args=(proxy,)).start()

    #return body.findall('div', {'class': 'freeProxyStyle'})
    #return re.findall(r'\d+\.\d+\.\d+\.\d+', body)




if __name__ == '__main__':
    #site = get_random_site()
    print(
        fetch_proxies(
            'https://proxy-daily.com/'
        )
    )

