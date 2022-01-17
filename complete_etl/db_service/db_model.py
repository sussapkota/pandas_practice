import configparser

from sqlalchemy import Column, BigInteger, String, Integer, create_engine,Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# style_id,gender,brand,style_name,color,image,attributes,price,quantity

class Shopping(Base):
    __tablename__ = 'restaurant'

    style_id = Column(BigInteger, primary_key=True)
    gender = Column(String)
    brand = Column(String)
    style_name = Column(String)
    color = Column(String)
    image = Column(String)
    attributes = Column(String)
    price = Column(Float)
    quantity = Column(Integer)

    def __init__(self, style_id, gender, brand, style_name, color, image, attributes, price, quantity):
        self.style_id = style_id
        self.gender = gender
        self.brand = brand
        self.style_name = style_name
        self.color = color,
        self.image = image
        self.attributes = attributes
        self.price = price
        self.quantity = quantity


config = configparser.ConfigParser()
config.read('config.env')

user = config['DB']['DB_USERNAME']
password = config['DB']['DB_PASSWORD']
ip = config['DB']['DB_IP']
dbase = config['DB']['DB_NAME']

engine = create_engine(f'postgresql://{user}:{password}@{ip}/{dbase}')

Base.metadata.create_all(engine)
