from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import csv

Base = declarative_base()
engine = create_engine('sqlite:///patients.db')

class Patient(Base):
    __tablename__ = 'patients'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    condition = Column(String)
    admission_date = Column(String)

Base.metadata.create_all(engine)

def init_db():
    with open('patients.csv', 'r') as f:
        csv_reader = csv.DictReader(f)
        with sessionmaker(bind=engine)() as session:
            for row in csv_reader:
                patient = Patient(**row)
                session.add(patient)
            session.commit()

def get_db():
    db = sessionmaker(bind=engine)()
    try:
        yield db
    finally:
        db.close()