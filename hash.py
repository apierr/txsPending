from bs4 import BeautifulSoup
import requests, re
from query import Query

class Hash:

    def __init__(self):
        txsLength = '20'
        self.url = 'https://www.etherchain.org/'
        self.txUrl = self.url + 'tx/'
        self.txsUrl = self.url + 'txs/pending/data?start=0&length=' + txsLength
        self.blockUrl = self.url + 'block/'

    def _getPendingTxs(self):
        r = requests.get(self.txsUrl)
        if r.status_code == 200:
            return r.json()['data']
        return []

    def _getNotConfirmedTxs(self):
        query = Query()
        return query.getNotConfirmedTxs()

    def _getHashFromHtml(self, row):
        return re.search('\w{64}', row['parenthash']).group(0)

    def _isConfirmedTx(self, txStatus):
        return 'Confirmation' in txStatus

    def _isPendingTx(self, txStatus):
        return 'Pending Transaction' in txStatus

    def _getSoup(self, url):
        response = requests.get(url)
        return BeautifulSoup(response.text, 'html.parser')

    def _getTimestamp(self, html):
        tr = str(html.findAll('table')[0].findAll('tr')[2])
        return re.search('\d{10}', tr).group(0)

    def _getBlockNumber(self, html):
        tr = str(html.findAll('table')[0].findAll('tr')[1])
        return re.search('\d{7}', tr).group(0)

    def _string2float(self, html):
        return float(re.search('\d+.\d+|\d+', html).group().replace(',','.'))

    def _getGasPrice(self, html):
        td = str(html.findAll('table')[0].findAll('tr')[8].find('td'))
        return self._string2float(td)

    def _getGasLimit(self, html):
        td = str(html.findAll('table')[0].findAll('tr')[9].find('td'))
        return self._string2float(td)

    def getTransactionDetails(self):
        for hash in self._getNotConfirmedTxs():
            return {
                'hash': hash,
                'blockTimestamp': self._getTimestamp(self._getSoup(self.txUrl + hash)),
                'blockId': self._getBlockNumber(self._getSoup(self.txUrl + hash)),
                'gasPrice': self._getGasPrice(self._getSoup(self.txUrl + hash)),
                'gasLimit': self._getGasLimit(self._getSoup(self.txUrl + hash))
            }

    def getHashes(self):
        pendingTxs = []
        for pendingTx in self._getPendingTxs():
            hash = self._getHashFromHtml(pendingTx)
            tableList = self._getSoup(self.txUrl + hash).findAll('table')
            if len(tableList) > 0:
                tr = tableList[0].findAll('tr')
                txStatus = str(tr[1])
                if self._isPendingTx(txStatus):
                    txTimestamp = str(tr[2])
                    pendingTxs.append([hash, self._getTimestamp(txTimestamp)])
        return pendingTxs
