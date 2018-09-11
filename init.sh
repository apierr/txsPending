
from dbSet import Base, Transaction
from dbPush import DbPush
from fetchTX import FetchTX

fetchTX = FetchTX()
dbPush = DbPush('tx.db')

txs = fetchTX.getPendingTx()
for tx in txs:
    print(tx)
    dbPush.set_tx(Transaction(address = tx[0], timestamp = tx[1], gasLimit = tx[2], gasPrice = tx[3]))
