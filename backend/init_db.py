from app import app, db
from models import User

# Use the application context
with app.app_context():
    # Create all tables in the database
    db.create_all()

    user = User(username='admin', password='password')
    db.session.add(user)
    db.session.commit()

print('Database initialized.')
