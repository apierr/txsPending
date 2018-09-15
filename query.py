from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
from dbSet import Transaction, Block

class Query:

    def __init__(self):
        engine = create_engine('sqlite:///tx.db')
        self.Session = sessionmaker(bind=engine)

    def getNotConfirmedTx(self):
        session = self.Session()
        for instance in session.query(Transaction)\
            .order_by(Transaction.id).filter(Transaction.blockId == -1).limit(1):
            return instance.hash

    def updateTxWithBlockId(self, dataTx):
        session = self.Session()
        session.query(Transaction)\
            .filter(Transaction.hash == dataTx['hash'])\
            .update({
                'blockId': dataTx['blockId'],
                'gasPrice': dataTx['gasPrice'],
                'gasLimit': dataTx['gasLimit']
            })
        session.commit()

    def getIdBlocks(self):
        idBlocks = []
        session = self.Session()
        sql = '''
            select distinct blockId from "transaction"
            where
                blockId > 1 and
                blockId not in (select id from "block");
        '''
        for idBlock in session.execute(sql):
            idBlocks.append(idBlock[0])
        session.commit()
        return idBlocks

    def insertBlock(self, block):
        session = self.Session()
        session.add(block)
        session.commit()
