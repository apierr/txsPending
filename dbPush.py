# Tested with Python 3.7
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dbSet import Base, Transaction

class DbPush:

    def __init__(self, db_name):
        self.db_name = db_name
        self.__set_session()

    def set_tx(self, data):
        self.session.add(data)
        self.session.commit()

    def __set_session(self):
        # TODO - the sqlite file should be taken from a configuration file since it appears in create_db.py, too.
        engine = create_engine('///'.join(['sqlite:', self.db_name]))
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()
