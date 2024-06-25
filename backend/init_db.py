from app import app, db
from models import User  # Import your models here

# Use the application context
with app.app_context():
    # Create all tables in the database
    db.create_all()

    # Add your initialization logic here
    # For example, create a new user
    user = User(username='admin', password='password')
    db.session.add(user)
    db.session.commit()

print('Database initialized.')
