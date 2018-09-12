from bs4 import BeautifulSoup
import requests, re

class Hash:

    def __init__(self):
        txsLength = '20'
        self.url = 'https://www.etherchain.org/'
        self.txUrl = self.url + 'tx/'
        self.txsUrl = self.url + 'txs/pending/data?start=0&length=' + txsLength

    def _getPendingTxs(self):
        r = requests.get(self.txsUrl)
        if r.status_code == 200:
            return r.json()['data']
        return []

    def _getHashFromHtml(self, row):
        return re.search('\w{64}', row['parenthash']).group(0)

    def _isPendingTx(self, txStatus):
        return 'Pending Transaction' in txStatus

    def _getSoup(self, url):
        response = requests.get(url)
        return BeautifulSoup(response.text, 'html.parser')

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
                    pendingTxs.append([hash, re.search('\d{10}', txTimestamp).group(0)])
        return pendingTxs
