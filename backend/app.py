from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token
from flask_cors import CORS
from sqlalchemy import text
from dotenv import load_dotenv
from sqlalchemy.dialects.postgresql import JSON
import mysql.connector
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
    __tablename__ = 'player'
    
    PlayerID = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Auto-increment primary key
    TeamID = db.Column(db.Integer, db.ForeignKey('team.TeamID'), nullable=True)  # Foreign key to the Team table
    NextGameStatus = db.Column(db.String(50), nullable=True)
    Position = db.Column(db.String(50), nullable=True)
    FirstName = db.Column(db.String(50), nullable=False)  # First name (required)
    LastName = db.Column(db.String(50), nullable=False)  # Last name (required)
    DraftAvailability = db.Column(db.Boolean, default=True)  # Draft availability (default True)
    ActivePlayerFlag = db.Column(db.Boolean, default=True)  # Active player flag (default True)
    Stats = db.Column(db.JSON, nullable=True)  # Player stats (JSON format)
    College = db.Column(db.String(100), nullable=True)  # College name
    InjuryHistory = db.Column(db.JSON, nullable=True)  # Injury history (JSON format)
    ImpactRating = db.Column(db.Numeric(3, 2), nullable=True)  # Impact rating for injuries (up to 3 digits, 2 decimal places)
    
    # Relationship to Team (if you have a Team model defined)
    team = db.relationship('Team', backref=db.backref('players', lazy=True), foreign_keys=[TeamID])


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
    RosterID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Foreign key referencing the Players table
    PlayerID = db.Column(db.Integer, db.ForeignKey('player.PlayerID'), nullable=False)
    
    # Foreign key referencing the User table
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'), nullable=False)
    
    # Relationship to the Players table (optional, if you want to access Player details from Roster)
    player = db.relationship('Player', backref=db.backref('rosters', lazy=True))
    
    # Relationship to the User table (optional, if you want to access User details from Roster)
    user = db.relationship('User', backref=db.backref('rosters', lazy=True))


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

        if bcrypt.check_password_hash(user.Password, password):
            return jsonify({
                'message': 'Login successful',
                'userID': user.UserID  # Include userID in the response
            }), 200
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
    
@app.route('/api/roster/<int:user_id>', methods=['GET'])
def get_roster(user_id):
    try:
        # Query to join Roster with Player based on UserID
        roster = Roster.query.filter_by(UserID=user_id).join(Player).all()
        
        # Build the data list with player details
        data = [
            {
                "PlayerID": roster_item.player.PlayerID, 
                "FirstName": roster_item.player.FirstName, 
                "LastName": roster_item.player.LastName, 
                "Position": roster_item.player.Position, 
                "TeamName": roster_item.player.team.TeamName if roster_item.player.team else None,
                "DraftAvailability": roster_item.player.DraftAvailability  # Include DraftAvailability

            }
            for roster_item in roster
        ]
        
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/roster', methods=['POST'])
def add_to_roster():
    data = request.json
    user_id = data.get('UserID')
    player_id = data.get('PlayerID')

    if not user_id or not player_id:
        return jsonify({'error': 'UserID and PlayerID are required'}), 400

    try:
        # Check if the player is available
        player = Player.query.get(player_id)
        if not player or not player.DraftAvailability or not player.ActivePlayerFlag:
            return jsonify({'error': 'Player is not available to add'}), 400
        
        # Set DraftAvailability to False to indicate that the player has been added to a roster
        player.DraftAvailability = False

        # Add the player to the roster
        new_roster_entry = Roster(UserID=user_id, PlayerID=player_id)
        db.session.add(new_roster_entry)
        db.session.commit()
        
        return jsonify({'message': 'Player added to roster'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/roster', methods=['DELETE'])
def remove_from_roster():
    data = request.json
    user_id = data.get('UserID')
    player_id = data.get('PlayerID')

    if not user_id or not player_id:
        return jsonify({'error': 'UserID and PlayerID are required'}), 400

    try:
        # Find the roster entry for the player
        roster_entry = Roster.query.filter_by(UserID=user_id, PlayerID=player_id).first()
        if not roster_entry:
            return jsonify({'error': 'Player not found on the roster'}), 404
        
        # Remove the player from the roster
        db.session.delete(roster_entry)
        db.session.commit()

        # Set the player's DraftAvailability to True
        player = Player.query.get(player_id)
        if player:
            player.DraftAvailability = True
            db.session.commit()

        return jsonify({'message': 'Player removed from roster and DraftAvailability set to True'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/available-players', methods=['GET'])
def get_available_players():
    try:
        players = Player.query.filter_by(DraftAvailability=True, ActivePlayerFlag=True).all()
        data = [
            {
                "PlayerID": player.PlayerID,
                "FirstName": player.FirstName,
                "LastName": player.LastName,
                "Position": player.Position,
                "TeamName": player.team.TeamName if player.team else None.__annotations,
                "DraftAvailability":player.DraftAvailability  # Include DraftAvailability
            }
            for player in players
        ]
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)