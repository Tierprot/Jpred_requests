from lxml import html
import requests
import os
import time

class seq_fetcher():
    # Fast and dirty fetcher
    # Pipeline:

    # job = seq_fetcher(sequence, job_name, download_dir) -->
    # job.push
    # while not job.results_url:
    #   job.check
    # job.pull

    #fast and dirty fetcher
    #cookies headers and other http junk
    cookies = {
        'jpredUserId': 'jpredUserId_1472020829YqIVeoPw',
        'jpredUserEmail': 'tierprot@gmail.com',
        '__utmt': '1',
        '__utma': '184934459.739022214.1472020684.1472020684.1472020684.1',
        '__utmb': '184934459.33.10.1472020684',
        '__utmc': '184934459',
        '__utmz': '184934459.1472020684.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    }

    headers = {
        'Origin': 'http://www.compbio.dundee.ac.uk',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryJBEI528TsFL54cYD',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Cache-Control': 'max-age=0',
        'Referer': 'http://www.compbio.dundee.ac.uk/jpred/',
        'Proxy-Connection': 'keep-alive',
    }

    def __init__(self, name, sequence, download_dir='download_dir'):
        self.seq = sequence
        self.name = name
        self.download_dir = os.path.join(os.getcwd(), download_dir)
        if not os.path.exists(self.download_dir):
            os.mkdir(self.download_dir)
        self.check_url = None
        self.results_url = None
        self.post_form = None
        self.complete = False

    #push sequnce and return url for checkout
    @property
    def push(self):
        post_form = '$------WebKitFormBoundaryJBEI528TsFL54cYD\r\nContent-Disposition: form-data; name="seq"' \
                    '\r\n\r\nsequence_placeholder\r\n------WebKitFormBoundaryJBEI528TsFL54cYD\r\nContent-Disposition: form-data; ' \
                    'name="fileup"; filename=""\r\nContent-Type: application/octet-stream\r\n\r\n\r\n------' \
                    'WebKitFormBoundaryJBEI528TsFL54cYD\r\nContent-Disposition: form-data; name="input"\r\n\r\nseq' \
                    '\r\n------WebKitFormBoundaryJBEI528TsFL54cYD\r\nContent-Disposition: form-data; name="pdb"\r\n\r\n' \
                    'on\r\n------WebKitFormBoundaryJBEI528TsFL54cYD\r\nContent-Disposition: form-data; name="email"' \
                    '\r\n\r\n\r\n------WebKitFormBoundaryJBEI528TsFL54cYD\r\nContent-Disposition: form-data; name="queryName"' \
                    '\r\n\r\n\r\n------WebKitFormBoundaryJBEI528TsFL54cYD--\r\n'

        self.post_form = post_form.replace('sequence_placeholder', self.seq)
        response = requests.post('http://www.compbio.dundee.ac.uk/jpred/cgi-bin/jpred_form',
                                 headers=self.headers, cookies=self.cookies, data=self.post_form)
        content = html.fromstring(response.text)
        self.check_url = content.xpath('//div[@id="content"]/p/a')[0].get('href')
        return content.xpath('//div[@id="content"]/p/a')[0].get('href')

    @property
    def check(self):
        if self.check_url:
            access = requests.get(self.check_url, allow_redirects=True)
            access = html.fromstring(access.text)
            try:
                url = access.xpath('//meta[@name="content"]')[0].attrib['content']
                url = url.split('=')[-1]
                self.results_url = url
                return True
            except Exception:
                return False
        else:
            print('no url to check yet provided')
            return False

    @property
    def pull(self):
        if self.results_url:
            access_url = self.results_url.replace('.results.html', '.tar.gz')
            access_url = requests.get(access_url, stream=True)
            filename = os.path.join(self.download_dir, self.name + '.tar.gz')
            with open(filename, 'wb') as output:
                for chunk in access_url.iter_content(chunk_size=1024, decode_unicode=False):
                    if chunk:
                        output.write(chunk)
            print('job {} is done'.format(self.name))
            self.complete = True
            return True
        else:
            return False


if __name__ == '__main__':
    sequence = 'VLSEGEWQLVLHVWAKVEADVAGHGQDILIRLFKSHPETLEKFDRFKHLKTEAEMKASEDLKKHGVTVLTALGAI' \
               'LKKKGHHEAELKPLAQSHIPIKYLEFISEAIIHVLHSRHPGDFGADAQGAMNIPIKYLEFISEAIIHVLHSRHPGDFGADAQGAMN' \
               'IPIKYLEFISEAIIHVLHSRHPGDFGADAQGAMNATKHKIPIKYLEFISEAIIHVLHSRHPGDFGADAQGAMNKALELFRKDIAAKYKELGYQG'
    AA = seq_fetcher(sequence=sequence, name='testfile')
    AA.push
    while not AA.results_url:
        AA.check
        time.sleep(1)
        print('waiting till completion')
    AA.pull

