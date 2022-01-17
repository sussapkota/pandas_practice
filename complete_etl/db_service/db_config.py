import configparser

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .db_model import Base, Shopping


class Database:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.env')

        user = config['DB']['DB_USERNAME']
        password = config['DB']['DB_PASSWORD']
        ip = config['DB']['DB_IP']
        dbase = config['DB']['DB_NAME']

        self.engine = create_engine(f'postgresql://{user}:{password}@{ip}/{dbase}')
        Base.metadata.bind = self.engine
        self.DBSession = sessionmaker(bind=self.engine)
        self.session = self.DBSession()

    def add(self, style_id, gender, brand, style_name, color, image, attributes, price, quantity):

        sec = self.session.query(Shopping).filter_by(style_id=style_id).first()
        if sec is None:
            sh1 = Shopping(style_id=style_id, style_name=style_name, quantity=quantity, attributes=attributes,
                           gender=gender, brand=brand, color=color,
                           image=image,
                           price=price)
            self.session.add(sh1)
            self.session.commit()
        else:
            print(f"Updating to the db with style_id {style_id}...")
            sec.style_name = style_name
            sec.quantity = quantity
            sec.attributes = attributes
            sec.gender = gender
            sec.brand = brand
            sec.color = color
            sec.image = image
            sec.price = price
            self.session.add(sec)
            self.session.commit()
