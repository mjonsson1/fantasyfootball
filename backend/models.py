from backend.app import db

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    team = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(20), nullable=False)
    draft_available = db.Column(db.Boolean, default=True) 
    is_active = db.Column(db.Boolean, default=True)
    # points = db.Column(db.Float, default=0.0)

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    owner = db.Column(db.String(80), nullable=False)
