import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import BTCData, Base

df = pd.read_csv('../data/BTC-USD.csv')

df['Date'] = pd.to_datetime(df['Date'])

# Drop the 'Adj Close' column
df.drop(columns=['adj close'], inplace=True)

df.columns = [col.lower() for col in df.columns]

print(df.head())

DATABASE_TYPE = 'postgresql'
DBAPI = 'psycopg2'
ENDPOINT = 'localhost'
USER = 'mela'
PASSWORD = 'mela'
PORT = 5432
DATABASE = 'bt'

connection_string = f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}"

engine = create_engine(connection_string)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

btc_data_list = [
    BTCData(
        date=row['date'],
        open=row['open'],
        high=row['high'],
        low=row['low'],
        close=row['close'],
        volume=row['volume'],
    ) for index, row in df.iterrows()
]

session.bulk_save_objects(btc_data_list)
session.commit()

print("Data loaded successfully!")
