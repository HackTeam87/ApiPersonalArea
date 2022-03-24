import sqlalchemy as db
from sqlalchemy.orm import relationship, backref
from datetime import datetime
now = datetime.now()
print(now)

from .db import Base



class Client(Base):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    company = db.Column(db.String)
    email = db.Column(db.String(50), unique=True)
    phone = db.Column(db.String(50))
    password = db.Column(db.String(50))
    balance = db.Numeric(14, 2)
    agents = relationship('Agent', backref='client', lazy=True)	

    def __repr__(self):
        return f'{self.balance}'


class Agent(Base):
    __tablename__ = 'agents'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    updated_at = db.Column(db.TIMESTAMP, default=datetime.timestamp(now) ) 
    created_at = db.Column(db.TIMESTAMP, default=datetime.timestamp(now) )
    uuid = db.Column(db.String,  unique=True )
    ip_address = db.Column(db.String, unique=True )
   
    def __repr__(self):
        return f'{self.ip_address}'


class Agent_Subscription(Base):
    __tablename__ = 'agent_subscriptions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at =  db.Column(db.TIMESTAMP, default=datetime.timestamp(now) )
    charged_amount = db.Column(db.String)
    expiried_at = db.Column(db.TIMESTAMP, default=datetime.timestamp(now))
    renew_automatically = db.Column(db.Boolean, nullable=True )
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'))
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscriptions.id'))

    def __repr__(self):
        return f'{self.renew_automatically}'


class Subscription(Base):
    __tablename__ = 'subscriptions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String)
    key = db.Column(db.String)
    name = db.Column(db.String)
    created_at = db.Column(db.TIMESTAMP, default=datetime.timestamp(now) )
    updated_at = db.Column(db.TIMESTAMP, default=datetime.timestamp(now) )
    changing_period = db.Column(db.String)
    charged_amount = db.Numeric(10, 2)
    components = db.Column(db.JSON, nullable=True)

    def __repr__(self):
        return f'{self.charged_amount}'


class Component(Base):
    __tablename__ = 'components'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.TIMESTAMP, default=datetime.timestamp(now) )
    updated_at = db.Column(db.TIMESTAMP, default=datetime.timestamp(now) ) 
    key = db.Column(db.String(100))
    achive_name = db.Column(db.String(150))
    description = db.Column(db.Text)
   
    def __repr__(self):
        return f'{self.description}'   

class Release(Base):
    __tablename__ = 'releases'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.TIMESTAMP, default=datetime.timestamp(now) )
    version = db.Column(db.String(50))
    changelog = db.Column(db.Text)
   
   
    def __repr__(self):
        return f'{self.changelog}' 


class Configuration(Base):
    __tablename__ = 'configuration'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    value = db.Column(db.Text)
   
   
    def __repr__(self):
        return f'{self.value}'         
   
# from .db import engine
# Base.metadata.create_all(bind=engine)


