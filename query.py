from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
from dbSet import Transaction


class Query:

    def __init__(self):
        engine = create_engine('sqlite:///tx.db')
        self.Session = sessionmaker(bind=engine)

    def getNotConfirmedTxs(self):
        hashes = []
        session = self.Session()
        for instance in session.query(Transaction)\
            .order_by(Transaction.id).filter(Transaction.blockId == -1).limit(1):
            hashes.append(instance.hash)
        return hashes

    def updateTxWithBlockId(self, txInfo):
        session = self.Session()
        session.query(Transaction)\
            .filter(Transaction.hash == txInfo['hash'])\
            .update({
                'blockId': txInfo['blockId'],
                'gasPrice': txInfo['gasPrice'],
                'gasLimit': txInfo['gasLimit']
            })
        session.commit()

query = Query()
print(query.getNotConfirmedTxs())
