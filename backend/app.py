from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token
from flask_cors import CORS
from sqlalchemy import text
from dotenv import load_dotenv
from sqlalchemy.dialects.postgresql import JSON
import re
import os

# Load environment variables
load_dotenv()
def get_db_credentials():
    credentials = {}
    try:
        with open("personalAuthentication.txt", "r") as file:
            for line in file:
                if line.strip():  # Ignore empty lines
                    key, value = line.strip().split("=")
                    credentials[key] = value
    except FileNotFoundError:
        raise Exception("personalAuthentication.txt not found.")

    return credentials
creds = get_db_credentials()
username = creds["username"]
password = creds["password"]
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{username}:{password}@localhost/test'
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Set a secure key for JWT
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
CORS(app)  # Enable CORS for all routes
migrate = Migrate(app, db)

# Helper function to convert SQLAlchemy rows to dictionaries
def row_to_dict(row):
    """Convert SQLAlchemy Row to dictionary using _mapping."""
    return dict(row._mapping)  # Use _mapping to access row data

class Team(db.Model):
    __tablename__ = 'team'

    # Primary key for Team table
    TeamID = db.Column(db.Integer, primary_key=True)

    # Team name (e.g., "Dallas Cowboys")
    TeamName = db.Column(db.String(100), nullable=False)

    # Team location (e.g., "Dallas, TX")
    TeamLocation = db.Column(db.String(100))

    # Coach of the team
    Coach = db.Column(db.String(100))

class Player(db.Model):
    __tablename__ = 'players'

    # Primary key for Player table
    PlayerID = db.Column(db.Integer, primary_key=True)

    # Foreign key referencing the Team table
    TeamID = db.Column(db.Integer, db.ForeignKey('team.TeamID'), nullable=False)

    # Next game status for the player
    NextGameStatus = db.Column(db.String(50))

    # Position of the player
    Position = db.Column(db.String(50))

    # First name and last name of the player
    FirstName = db.Column(db.String(50), nullable=False)
    LastName = db.Column(db.String(50), nullable=False)

    # Whether the player is available for the draft
    DraftAvailability = db.Column(db.Boolean, default=True)

    # Whether the player is an active player
    ActivePlayerFlag = db.Column(db.Boolean, default=True)

    # Stats of the player in JSON format
    Stats = db.Column(JSON)

    # College the player attended
    College = db.Column(db.String(100))

    # Injury history (for injury impact analyzer)
    InjuryHistory = db.Column(JSON)

    # Impact rating for injuries (a decimal with 2 digits after the decimal point)
    ImpactRating = db.Column(db.Numeric(3, 2))

    # Relationship to the Team table
    team = db.relationship('Team', backref=db.backref('players', lazy=True))


# User model for database
class User(db.Model):
    __tablename__ = 'user'
    
    UserID = db.Column(db.Integer, primary_key=True)  # Corresponds to the UserID column in the table
    FirstName = db.Column(db.String(50), nullable=False)
    LastName = db.Column(db.String(50), nullable=False)
    Birthdate = db.Column(db.Date, nullable=False)
    Age = db.Column(db.Integer)
    Email = db.Column(db.String(100), unique=True, nullable=False)
    Username = db.Column(db.String(50), unique=True, nullable=False)
    Record = db.Column(db.String(10))
    Password = db.Column(db.String(255), nullable=False)

class Roster(db.Model):
    __tablename__ = 'roster'
    # Primary key for Roster table
    RosterID = db.Column(db.Integer, primary_key=True)
    # Foreign key referencing the Players table
    PlayerID = db.Column(db.Integer, db.ForeignKey('players.PlayerID'), nullable=False)
    # Relationship to the Players table (optional, if you want to access Player details from Roster)
    player = db.relationship('Player', backref=db.backref('rosters', lazy=True))

# Route to get players
@app.route('/api/players', methods=['GET'])
def get_players():
    try:
        with db.engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM players;"))
            data = [row_to_dict(row) for row in result]
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to test database connection
@app.route('/test-connection')
def test_connection():
    try:
        with db.engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM player;"))
            data = [row_to_dict(row) for row in result]
            return {"status": "success", "data": data}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

# Registration route: Hash password before storing
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    print(data)
    # Validate required fields
    required_fields = ['FirstName', 'LastName', 'Username', 'Birthdate', 'Age', 'email', 'password' ]
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"error": f"{field} is required"}), 400

    # Validate email format
    email_regex = r"(^[a-z0-9]+([.-_][a-z0-9]+)*@[a-z0-9-]+(\.[a-z]{2,})$)"
    if not re.match(email_regex, data['email']):
        return jsonify({"error": "Invalid email format"}), 400

    # Validate password strength (at least 8 characters, one number, and one uppercase letter)
    if len(data['password']) < 8 or not any(char.isdigit() for char in data['password']) or not any(char.isupper() for char in data['password']):
        return jsonify({"error": "password must be at least 8 characters long, include a number and an uppercase letter"}), 400

    # Hash the password
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    # Proceed with registration logic if validation passes
    try:
        new_user = User(
            FirstName=data['FirstName'],
            LastName=data['LastName'],
            Birthdate=data['Birthdate'],
            Age=data['Age'],
            Email=data['email'],
            Username=data['Username'],
            Record=data.get('Record', '0-0'),  # Default value if not provided
            Password=hashed_password  # Store hashed password
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error: {str(e)}")  # Log the error
        return jsonify({"error": "An error occurred during registration"}), 500
    
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

    user = User.query.filter_by(Email=email).first()

    if user:
        # Debugging: Print the stored hash and entered password
        print(f"Stored hash: {user.Password}")
        print(f"Entered password: {password}")

        # bcrypt will automatically extract the salt from the stored hash
        if bcrypt.check_password_hash(user.Password, password):
            return jsonify({'message': 'Login successful'}), 200
        else:
            return jsonify({'message': 'Invalid email or password'}), 401
    else:
        return jsonify({'message': 'User not found'}), 404


@app.route('/api/reset-password', methods=['POST'])
def reset_password():
    data = request.json

    # Check if both email and new password are provided
    if 'email' not in data or 'new_password' not in data:
        return jsonify({"error": "Email and new password are required"}), 400

    email = data['email']
    new_password = data['new_password']

    # Find the user by email
    user = User.query.filter_by(Email=email).first()

    if user:
        # Hash the new password
        hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')

        try:
            # Update the user's password
            user.Password = hashed_password
            db.session.commit()
            return jsonify({"message": "Password has been updated successfully"}), 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "User not found"}), 404
    


if __name__ == '__main__':
    app.run(debug=True)

