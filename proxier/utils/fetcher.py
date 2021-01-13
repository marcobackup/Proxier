
from proxier.utils import *


class Fetcher:

    def __init__(self, proxy_sites):
        self.PROXY_SITES = proxy_sites
        self.PATTERN     = r'(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3}):(\d{1,5})'
        self.FILE_NAME   = 'proxy.zip'

    def get_proxies_sites(self):
        return self.PROXY_SITES

    def worker(self, site, result, cookies=None):
        res = requests.get(
            site,
            cookies=cookies,
            headers=HEADERS,
            timeout=TIMEOUT
        )
        if res.status_code == requests.codes.ok:
            result.append(res)

    def workupload_downloader(self, download_id):
        token_id = []
        self.worker(
            f'https://workupload.com/file/{download_id}',
            token_id
        )
        token_id    = token_id[0].cookies['token']
        temp_result = []
        self.worker(
            f'https://workupload.com/start/{download_id}',
            temp_result,
            {'token': token_id}
        )
        if temp_result[0].status_code == requests.codes.ok:
            temp_result = []
            self.worker(
                f'https://workupload.com/api/file/getDownloadServer/{download_id}',
                temp_result,
                {'token': token_id}
            )
            temp_result = temp_result[0].json()
            if temp_result['success']:
                result = []
                self.worker(
                    temp_result['data']['url'],
                    result,
                    {'token': token_id}
                )
                yield result[0]

    def fetch_proxy(self, site):
        try:
            res = []
            th = threading.Thread(target=self.worker, args=(site, res,))
            th.start()
            th.join()
            for _ in res:
                _ = _.text
                html = BeautifulSoup(_, 'html.parser')
                posts = html.find_all('h3', {'class': 'post-title'})
                if len(posts) > 0:
                    for post in posts:
                        post = post.select('.post-title a')[0]['href']
                        fetched = re.findall(self.PATTERN, requests.get(post).text)
                        if len(fetched) > 0:
                            for proxy in fetched:
                                yield '.'.join(proxy[:len(proxy)-1]) + f':{proxy[len(proxy)-1]}'
                        else:
                            post = requests.get(post).text
                            download_id = post.split('="https://workupload.com/')[1].split('" ')[0].split('/')[1]
                            for _ in self.workupload_downloader(download_id):
                                with open(self.FILE_NAME, 'wb') as zip_file:
                                    zip_file.write(_.content)
                                    zip_file.close()     
                                    archive = zipfile.ZipFile('proxy.zip')
                                    for _ in archive.namelist():
                                        if '.txt' in _:
                                            fetched = re.findall(self.PATTERN, archive.read(_).decode())
                                            for proxy in fetched:
                                                yield '.'.join(proxy[:len(proxy)-1]) + f':{proxy[len(proxy)-1]}'
                                    archive.close()
                                    os.remove(self.FILE_NAME)  
                else:
                    fetched = re.findall(self.PATTERN, _)
                    for proxy in fetched:
                        yield '.'.join(proxy[:len(proxy)-1]) + f':{proxy[len(proxy)-1]}'
        except Exception as e:
            yield False


        