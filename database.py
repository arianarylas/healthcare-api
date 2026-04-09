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
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            for row in csv_reader:
                # Check if the patient already exists by ID
                existing_patient = session.query(Patient).filter_by(id=row['id']).first()
                if not existing_patient:
                    patient = Patient(**row)
                    session.add(patient)
            session.commit()
        except Exception as e:
            print(f"Error seeding database: {e}")
            session.rollback()
        finally:
            session.close()

def get_db():
    db = sessionmaker(bind=engine)()
    try:
        yield db
    finally:
        db.close()