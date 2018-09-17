import requests, re
from query import Query
from htmlParser import HtmlParser

class Hash:

    def __init__(self):
        self.url = 'https://www.etherchain.org/'
        self.blockUrl = self.url + 'block/'

    def _getNotConfirmedTx(self):
        query = Query()
        return query.getNotConfirmedTx()

    def _getHashFromHtml(self, row):
        return re.search('\w{64}', row['parenthash']).group(0)

    def _getFakeDataTx(self, hash):
        return {
            'hash': hash,
            'blockId': 1,
            'gasPrice': -1,
            'gasLimit': -1
        }

    def getTxsData(self):
        hash = self._getNotConfirmedTx()
        print(hash)
        htmlParser = HtmlParser(hash)
        if hasattr(htmlParser, 'tableText'):
            return {
                'hash': hash,
                'blockId': htmlParser.getBlockNumber(),
                'gasPrice': htmlParser.getGasPrice(),
                'gasLimit': htmlParser.getGasLimit()
            }
        return self._getFakeDataTx(hash)

    def getPendingTxsHashes(self):
        pendingTxs = []
        htmlParser = HtmlParser()
        for pendingTx in htmlParser.getPendingTxs():
            hash = self._getHashFromHtml(pendingTx)
            htmlParser = HtmlParser(hash)
            print(hash)
            if hasattr(htmlParser, 'tableText'):
                pendingTxs.append([hash, htmlParser.getTimestamp()])
        return pendingTxs
