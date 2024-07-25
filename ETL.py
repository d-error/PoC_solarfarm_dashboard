import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, MetaData, Table
from sqlalchemy.orm import sessionmaker, declarative_base

from packages.extractor import extract_from_caleb_excel

path_to_excel = './data/Tracker data 20240528.xlsx'

df = extract_from_caleb_excel(path_to_excel)

# Process DataFrame
records = []
for index, row in df.iterrows():
    timestamp = row['Timestamp']
    for col in df.columns:
        if col != 'Timestamp':
            tracker_id = col.split('[')[-1].replace(']', '').replace('Tracker ', '')
            value = row[col]
            records.append({'timestamp': timestamp, 'tracker_id': tracker_id, 'value': value})

# Convert records to DataFrame
processed_df = pd.DataFrame(records)

processed_df.to_csv('data/processed_data.csv')
# SQLAlchemy setup
Base = declarative_base()

class TrackerData(Base):
    __tablename__ = 'tracker_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(DateTime, nullable=False)
    tracker_id = Column(String, nullable=False)
    value = Column(Float, nullable=False)

# PostgreSQL database connection
DATABASE_URI = 'postgresql+psycopg2://docker:password@localhost:5432/grafana'
engine = create_engine(DATABASE_URI)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Insert data into the database
for index, row in processed_df.iterrows():
    record = TrackerData(time=row['timestamp'], tracker_id=row['tracker_id'], value=row['value'])
    session.add(record)

session.commit()
session.close()
