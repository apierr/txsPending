
from dbSet import Base, Transaction
from dbPush import DbPush
from fetchTX import FetchTX
from hash import Hash
import time

fetchTX = FetchTX()
dbPush = DbPush('tx.db')


def run():
    hash = Hash()
    print(hash.getHashes())
    for hash in hash.getHashes():
        dbPush.set_tx(Transaction(
            hash = hash[0],
            timestamp = hash[1],
            gasLimit = -1,
            gasPrice = -1
        ))

while True:
    run()
    time.sleep(10)
