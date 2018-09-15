
from dbSet import Base, Transaction, Block
from dbPush import DbPush
from hash import Hash
import time
from query import Query
from htmlParser import HtmlParser

dbPush = DbPush('tx.db')
query = Query()
hash = Hash()

def _getPendingTxsHashes():
    hash = Hash()
    print(hash.getPendingTxsHashes())
    for hash in hash.getPendingTxsHashes():
        dbPush.set_tx(Transaction(
            hash = hash[0],
            timestamp = hash[1],
            gasLimit = -1,
            gasPrice = -1
        ))

def getPendingTxsHashes():
    while True:
        _getPendingTxsHashes()
        time.sleep(10)

def updateTxWithBlockId():
    for i in range (0, 50):
        txData = hash.getTxsData()
        print(txData)
        query.updateTxWithBlockId(txData)

def updateBlockTable():
    for blockId in query.getIdBlocks():
        print(blockId)
        htmlParser = HtmlParser(str(blockId))
        blockInfo = htmlParser.getBlock()
        query.insertBlock(Block(
            id = blockId,
            hash = '',
            timestamp = blockInfo['timestamp'],
            minedIn = blockInfo['minedIn']
        ))

#getPendingTxsHashes()
#updateTxWithBlockId()
updateBlockTable()
