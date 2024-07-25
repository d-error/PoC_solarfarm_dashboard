import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, MetaData, Table
from sqlalchemy.orm import sessionmaker, declarative_base

# Sample DataFrame
# data = {
#     'Timestamp': ['2024-05-28 06:00:00', '2024-05-28 06:05:00', '2024-05-28 06:10:00', '2024-05-28 06:15:00', '2024-05-28 06:20:00', '2024-05-28 06:25:00'],
#     'Current roll (degrees) [Tracker TCU-087-001]': [5.8, 5.8, 5.8, 5.8, 5.8, 5.8],
#     'Current roll (degrees) [Tracker TCU-087-002]': [5.8, 5.8, 5.8, 5.8, 5.8, 5.8]
# }

# df = pd.DataFrame(data)
# df['Timestamp'] = pd.to_datetime(df['Timestamp'])
df = pd.read_csv('data_sample.csv')

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

processed_df.to_csv('processed_data.csv')
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
