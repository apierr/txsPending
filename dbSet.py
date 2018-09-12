import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import Boolean, Numeric, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Transaction (Base):
    __tablename__ = 'transaction'
    # Here we define columns for the table person
    id = Column(Integer, primary_key = True)
    hash = Column(String(250), unique = False)
    timestamp = Column(Integer, nullable = False)
    gasLimit = Column(Integer, nullable = True)
    gasPrice = Column(Numeric, nullable = True)
# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///tx.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
