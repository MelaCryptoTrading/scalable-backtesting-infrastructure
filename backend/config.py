import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:15433/btc'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', '6fbb3c6d4c42c9c0d4fd7edb60a3a99b32ab798d9ef0b847e5e91765f5eb4d92')
