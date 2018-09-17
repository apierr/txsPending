from bs4 import BeautifulSoup
import requests, re

class HtmlParser:

    def __init__(self, hash = ''):
        txsLength = '10'
        self.soup = None
        self.hash =  hash
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
        if self.soup.find('table'):
            self.tableText = self.soup.find('table').text
            self.tableSource = str(self.soup.find('table'))

    def _string2float(self, html):
        return float(re.search('\d+.\d+|\d+', html).group().replace(',',''))

    def _reSearch(self, regExp):
        reSearch = re.search(regExp, self.tableText)
        if hasattr(reSearch, 'group'):
            return reSearch.group(1)
        return 0

    def getPendingTxs(self):
        r = requests.get(self.txsUrl)
        if r.status_code == 200:
            return r.json()['data']
        return []

    def getTimestamp(self):
        return re.search('aria-ethereum-date="(\d{10})"', self.tableSource).group(1)

    def isPendingTx(self):
        return 'Pending Transaction' in self.tableText

    def getBlockNumber(self):
        block = re.search('Block(\d{7})', self.tableText)
        if block == None:
            return 1
        return block.group(1)

    def getGasPrice(self):
        value = re.search('Gas Price(\d+.\d+|\d+) GWei', self.tableText).group(1)
        return self._string2float(value)

    def getGasLimit(self):
        value = re.search('Gas Limit(\d+.\d+|\d+)', self.tableText).group(1)
        return self._string2float(value)

    def getBlock(self):
        return {
            'minedIn': int(self._reSearch('Mined in (\d+)s')),
            'timestamp': int(re.search('aria-ethereum-date="(\d{10})"', self.tableSource).group(1))
        }

    def isTable(self):
        return len(self.soup.findAll('table')) > 0
