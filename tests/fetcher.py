
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


def worker(url, stream=False, cookies=None, headers=None):
    return requests.get(
        url,
        cookies=cookies,
        headers=headers,
        stream=stream
    )

def fetch_with_download(url):
    proxies = []
    res = worker(url)
    body = BeautifulSoup(res.text, 'html.parser')
    posts = body.find_all('h3', {'class': 'post-title'})
    if len(posts) > 0:
        for post in posts:
            post = post.select('.post-title a')[0]['href']
            post = worker(post).text
            proxies_ = re.findall(
                r'(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3}):(\d{1,5})', 
                post
            )
            if len(proxies_) > 0:
                for proxy in proxies_:
                    proxies.append('.'.join(proxy[:len(proxy)-1]) + f':{proxy[len(proxy)-1]}')
            else:
                user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'
                download = post.split('="https://workupload.com/')[1].split('" ')[0].split('/')[1]
                cookie = worker(f'https://workupload.com/file/{download}', headers={'User-Agent': user_agent}).cookies['token']
                start = worker(f'https://workupload.com/start/{download}', cookies={'token': cookie}, headers={'User-Agent': user_agent})
                res = worker(f'https://workupload.com/api/file/getDownloadServer/{download}', cookies={'token': cookie}, headers={'User-Agent': user_agent}).json()
                if res['success']: res = worker(res['data']['url'], True, cookies={'token': cookie}, headers={'User-Agent': user_agent})
                if bytes is type(res.content):
                    with open(f'proxy.zip', 'wb') as _file:
                        _file.write(res.content)
                        _file.close()
                        import zipfile, os
                        archive = zipfile.ZipFile('proxy.zip')
                        for _ in archive.namelist():
                            if '.txt' in _:
                                proxies_ = re.findall(
                                    r'(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3}):(\d{1,5})', 
                                    archive.read(_).decode()
                                )
                                for proxy in proxies_:
                                    proxies.append('.'.join(proxy[:len(proxy)-1]) + f':{proxy[len(proxy)-1]}')
                        archive.close()
                        os.remove('proxy.zip')

        print(len(proxies))


if __name__ == '__main__':
    print(
        fetch_with_download(
            #'http://www.live-socks.net/'
            #'http://www.vipsocks24.net/'
            #'http://www.proxyserverlist24.top/'
            #'http://newfreshproxies-24.blogspot.com'
            #'http://www.freshnewproxies24.top/'
            #'http://www.socks24.org/'
            'http://www.socksproxylist24.top/'
        )
    )

