from app import app, db
from models import Userss

with app.app_context():
    db.create_all()

    if not Userss.query.filter_by(username='admin').first():
        user = Userss(username='admin')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()

print('Database initialized.')
