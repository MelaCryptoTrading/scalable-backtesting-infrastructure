import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:15433/btc'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
