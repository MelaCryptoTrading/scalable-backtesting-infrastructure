from app import app, db
from models import Userss

# Use the application context
with app.app_context():
    # Create all tables in the database
    db.create_all()

    user = Userss(username='admin', password='password')
    db.session.add(user)
    db.session.commit()

print('Database initialized.')
