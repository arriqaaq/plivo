import sys
from sqlalchemy import Integer, ForeignKey, String, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Call(Base):
	__tablename__='call'
	name=Column(String(80),nullable=False)
	id=Column(Integer,primary_key=True)
	status=Column(String(80),nullable=False)
	busy=Column(Integer,nullable=False)
#End code
engine=create_engine('sqlite:///call.db')
Base.metadata.create_all(engine)