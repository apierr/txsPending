
from dbSet import Base, Transaction
from dbPush import DbPush
from hash import Hash
import time
from query import Query

dbPush = DbPush('tx.db')
hash = Hash()
query = Query()

def run():

    print(hash.getHashes())
    for hash in hash.getHashes():
        dbPush.set_tx(Transaction(
            hash = hash[0],
            timestamp = hash[1],
            gasLimit = -1,
            gasPrice = -1
        ))

# while True:
#     run()
#     time.sleep(10)
query.updateTxWithBlockId(hash.getTransactionDetails())
