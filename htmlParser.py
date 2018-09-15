from bs4 import BeautifulSoup
import requests, re

class HtmlParser:

    def __init__(self, hash = ''):
        txsLength = '20'
        self.soup = None
        self.hash = hash
        self.url = 'https://www.etherchain.org/'
        self.txsUrl = self.url + 'txs/pending/data?start=0&length=' + txsLength
        self.txUrl = self.url + 'tx/'
        if len(hash) == 64:
            self._setSoup(self.txUrl + self.hash)
        elif len(hash) == 7:
            self._setSoup(self.url + 'block/' + self.hash)

    def _setSoup(self, url):
        response = requests.get(url)
        self.soup = BeautifulSoup(response.text, 'html.parser')

    def _getTrTable(self, html):
        return html.findAll('table')[0].findAll('tr')

    def _string2float(self, html):
        return float(re.search('\d+.\d+|\d+', html).group().replace(',',''))

    def getPendingTxs(self):
        r = requests.get(self.txsUrl)
        if r.status_code == 200:
            return r.json()['data']
        return []

    def getSoup(self):
        url = self.txUrl + self.hash
        response = requests.get(url)
        return self.soup

    def getTimestamp(self):
        tr = str(self.soup.findAll('table')[0].findAll('tr')[2])
        return re.search('\d{10}', tr).group(0)

    def isPendingTx(self):
        txStatus = str(self.soup.findAll('table')[0].findAll('tr')[1])
        return 'Pending Transaction' in txStatus

    def getBlockNumber(self):
        tr = str(self.soup.findAll('table')[0].findAll('tr')[1])
        print("re.search('\d{7}', tr)", re.search('\d{7}', tr))
        if re.search('\d{7}', tr) == None:
            return 1
        return re.search('\d{7}', tr).group(0)

    def getGasPrice(self):
        value = re.search('Gas Price(\d+.\d+|\d+) GWei', self.soup.find('table').text).group(1)
        return self._string2float(value)

    def getGasLimit(self):
        value = re.search('Gas Limit(\d+.\d+|\d+)',self.soup.find('table').text).group(1)
        return self._string2float(value)

    def getBlock(self):
        tr = self.soup.findAll('table')[0].findAll('tr')
        return {
            'minedIn': int(re.search("Mined in (\d+)s", str(tr[2])).group(1)),
            'timestamp': int(re.search('aria-ethereum-date="(\d{10})"', str(tr[9])).group(1))
        }

    def isTable(self):
        return len(self.soup.findAll('table')) > 0
