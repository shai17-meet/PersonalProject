from sqlalchemy import Column,Integer,String, DateTime, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, func, DateTime

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}  #This will enable us to add more columns later
    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)
    email = Column(String)
    photo = Column(String)
    threads= relationship("Thread", back_populates="user")
    comments= relationship("Comment", back_populates="user")

    def verify_password(self, password_attempt):
    	return self.password==password_attempt

class Thread(Base):
    __tablename__ = 'thread'
    __table_args__ = {'extend_existing': True}
    id=Column(Integer, primary_key=True)
    title=Column(String)
    text=Column(String)
    user_id=Column(Integer, ForeignKey('user.id'))
    timestamp=Column(DateTime, default=func.now())
    photo=Column(String)
    topic=Column(String)
    comments=relationship("Comment", back_populates="thread")
    user=relationship("User", back_populates="threads")


class Comment(Base):
    __tablename__ = 'comment'
    __table_args__ = {'extend_existing': True}
    id=Column(Integer, primary_key=True)
    user_id=Column(Integer, ForeignKey('user.id'))
    text=Column(String)
    timestamp=Column(DateTime, default=func.now())
    thread_id=Column(Integer, ForeignKey('thread.id'))
    user=relationship("User", back_populates="comments")
    thread=relationship("Thread", back_populates="comments")


engine = create_engine('sqlite:///forum.db')
Base.metadata.create_all(engine)
Base.metadata.bind= engine
DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()


    		
    

