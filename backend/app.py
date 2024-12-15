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
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{username}:{password}@localhost/FINAL_NFL_STATS'
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


class Player(db.Model):
    __tablename__ = 'players'

    # Primary key for Player table
    PlayerID = db.Column(db.Integer, primary_key=True)

    # Foreign key referencing the Team table
    TeamAB = db.Column(db.String(3))

    # Next game status for the player
    # NextGameStatus = db.Column(db.String(50))

    # Position of the player
    Position = db.Column(db.String(50))

    # First name and last name of the player
    # FirstName = db.Column(db.String(50), nullable=False)
    # LastName = db.Column(db.String(50), nullable=False)
    PlayerName = db.Column(db.String(50))
    # Whether the player is available for the draft
    DraftAvailability = db.Column(db.Boolean, default=True)

    # Whether the player is an active player
    ActivePlayerFlag = db.Column(db.Boolean, default=True)
    stats = db.relationship('Stats', back_populates='player', overlaps='stats')
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
    
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'), nullable=False)
    # Foreign key referencing the Players table
    PlayerID = db.Column(db.Integer, db.ForeignKey('players.PlayerID'), nullable=False)
    # Relationship to the Players table (optional, if you want to access Player details from Roster)
    user = db.relationship('User', backref=db.backref('rosters', lazy=True))
    player = db.relationship('Player', backref=db.backref('rosters', lazy=True))

class Stats(db.Model):
    __tablename__ = 'STATS'
    GameID = db.Column(db.Integer, primary_key=True)
    PlayerID = db.Column(db.Integer, db.ForeignKey('players.PlayerID'), primary_key=True)  # Foreign key to Player table
    PlayerName = db.Column(db.String(100))
    TeamAB = db.Column(db.String(3))
    Position = db.Column(db.String(20))
    StatType = db.Column(db.String(50))
    PassingYards = db.Column(db.Integer)
    PassingTouchdowns = db.Column(db.Integer)
    Interceptions = db.Column(db.Integer)
    AdjQBR = db.Column(db.Float)
    RushingYards = db.Column(db.Integer)
    RushingTouchdowns = db.Column(db.Integer)
    Receptions = db.Column(db.Integer)
    ReceivingYards = db.Column(db.Integer)
    ReceivingTouchdowns = db.Column(db.Integer)
    Fumbles = db.Column(db.Integer)
    FumblesLost = db.Column(db.Integer)
    FumblesRecovered = db.Column(db.Integer)
    TotalTackles = db.Column(db.Float)
    Sacks = db.Column(db.Float)
    PassesDefended = db.Column(db.Integer)
    DefensiveTouchdowns = db.Column(db.Integer)
    # InterceptionsDefensive = db.Column(db.Integer)
    InterceptionYards = db.Column(db.Float)
    InterceptionTouchdowns = db.Column(db.Integer)
    KickReturns = db.Column(db.Integer)
    KickReturnYards = db.Column(db.Integer)
    KickReturnTouchdowns = db.Column(db.Integer)
    PuntReturns = db.Column(db.Integer)
    PuntReturnYards = db.Column(db.Integer)
    PuntReturnTouchdowns = db.Column(db.Integer)
    FieldGoalsMade = db.Column(db.Integer)
    ExtraPointsMade = db.Column(db.Integer)
    TotalKickingPoints = db.Column(db.Integer)
    Punts = db.Column(db.Integer)
    PuntYards = db.Column(db.Integer)
    GrossAvgPuntYards = db.Column(db.Float)
    Touchbacks = db.Column(db.Integer)
    PuntsInside20 = db.Column(db.Integer)
    Completions = db.Column(db.Integer)
    Week = db.Column(db.Integer)
    player = db.relationship('Player', back_populates='stats', overlaps='player_stats')
# Route to get players
@app.route('/api/players', methods=['GET'])
def get_players():
    try:
        with db.engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM players WHERE DraftAvailability = True ORDER BY Position ASC, PlayerName ASC;"))

            # Ensure each row is being converted into a dictionary with correct keys
            data = [row_to_dict(row) for row in result]
            # print(data)  # Log the data to check the structure
        return jsonify(data), 200
    except Exception as e:
        print(f"Error: {str(e)}")  # Log the error to debug it
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
            return jsonify({'message': 'Login successful','userID': user.UserID}),200  # Include userID in the response)
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
        # Query to join Roster, Player, based on user ID
        query = """
        SELECT r.UserID, p.PlayerID, p.PlayerName, p.Position, p.TeamAB
        FROM Roster r
        JOIN Players p ON r.PlayerID = p.PlayerID
        WHERE r.UserID = :user_id
        """
        
        with db.engine.connect() as connection:
            result = connection.execute(text(query), {"user_id": user_id})
            data = [row_to_dict(row) for row in result]

        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/roster', methods=['POST'])
def add_to_roster():
    try:
        data = request.json
        user_id = data.get('UserID')
        player_id = data.get('PlayerID')
        print("received api user id", user_id)
        print("received player id", player_id)

        if not user_id or not player_id:
            return jsonify({'error': 'UserID and PlayerID are required'}), 400

        player = Player.query.get(player_id)
        if not player:
            return jsonify({'error': 'Player not found'}), 400

        print("player draft availability", player.DraftAvailability)

        # Continue with your roster size logic...
        current_roster_size = Roster.query.filter_by(UserID=user_id).count()
        max_roster_size = 50 # Example limit

        if current_roster_size >= max_roster_size:
            return jsonify({'error': 'Roster limit reached. Cannot add more players.'}), 400

        if not player.DraftAvailability or not player.ActivePlayerFlag:
            return jsonify({'error': 'Player is not available to add'}), 400

        player.DraftAvailability = False
        new_roster_entry = Roster(UserID=user_id, PlayerID=player_id)
        db.session.add(new_roster_entry)
        db.session.commit()

        return jsonify({
            'message': 'Player added to roster',
            'PlayerID': player.PlayerID,
            'PlayerName': player.PlayerName,
            'Position': player.Position,
            'TeamAB': player.TeamAB,
            'DraftAvailability': player.DraftAvailability
        }), 201

    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Log error to backend
        db.session.rollback()
        return jsonify({'error': 'Internal Server Error. Please try again.'}), 500

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

        return jsonify({'message': f'{player.PlayerName} has been removed from your roster'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/roster_size', methods=['GET'])
def get_roster_size():
    try:
        user_id = request.args.get('UserID')  # Get UserID from query parameters
        if not user_id:
            return jsonify({'error': 'UserID is required'}), 400

        current_roster_size = Roster.query.filter_by(UserID=user_id).count()
        max_roster_size = 50  # Example max roster size

        return jsonify({'current_roster_size': current_roster_size, 'max_roster_size': max_roster_size}), 200

    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Log error to backend
        return jsonify({'error': 'Internal Server Error. Please try again.'}), 500

    
# INJURY IMPACT ANALYZER
    
@app.route('/api/injury-impact', methods=['POST'])
def injury_impact_analyzer():
    data = request.json
    user_id = data.get('userID')
    player_ids = data.get('PlayerIDs')  # List of selected player IDs

    if not user_id or not player_ids:
        return jsonify({'error': 'UserID and PlayerIDs are required'}), 400

    try:
        # Fetch the historical stats for the selected players
        players_stats = Stats.query.filter(Stats.PlayerID.in_(player_ids)).all()

        # Define the scoring weights
        scoring_weights = {
            'Completions': 0.5,
            'PassingYards': 0.04,
            'PassingTouchdowns': 4,
            'Interceptions': -2,
            'Sacks': -1,
            'AdjQBR': 0.1,
            'RushingYards': 0.1,
            'RushingTouchdowns': 6,
            'Receptions': 1,
            'ReceivingYards': 0.1,
            'ReceivingTouchdowns': 6,
            'Fumbles': -1,
            'FumblesLost': -1,
            'FumblesRecovered': 1,
            'TotalTackles': 1,
            'PassesDefended': 2,
            'DefensiveTouchdowns': 6,
            # 'InterceptionsDefensive': 2,
            'InterceptionYards': 0.1,
            'InterceptionTouchdowns': 6,
            'KickReturns': 0.5,
            'KickReturnYards': 0.1,
            'KickReturnTouchdowns': 6,
            'PuntReturns': 0.5,
            'PuntReturnYards': 0.1,
            'PuntReturnTouchdowns': 6,
            'FieldGoalsMade': 3,
            'ExtraPointsMade': 1,
            'TotalKickingPoints': 1,
            'Punts': 0.1,
            'PuntYards': 0.05,
            'GrossAvgPuntYards': 0.05,
            'Touchbacks': 1,
            'PuntsInside20': 0.5,
        }


        # Calculate the total score for all selected players
        # Calculate the total score for all selected players
        player_scores = {}

        for stat in players_stats:
            player_id = stat.PlayerID

            if player_id not in player_scores:
                player_scores[player_id] = {'total_score': 0, 'game_count': 0}

            # Reset game score at the start of each game iteration
            game_score = 0
            
            for key, weight in scoring_weights.items():
                value = getattr(stat, key, None)
                value = value or 0  # Default value for None stats
                game_score += value * weight  # Add to the game score

            # Update the player's total score after calculating the game score
            player_scores[player_id]['total_score'] += game_score
            player_scores[player_id]['game_count'] += 1


        # Calculate average scores and sum them up for the total score
        total_score = 0
        for player_id, scores in player_scores.items():
            if scores['game_count'] > 0:
                average_score = scores['total_score'] / scores['game_count']
                total_score += average_score
                print(f"PlayerID: {player_id}, Average Score: {average_score}")
            else:
                print(f"Warning: Player {player_id} has no games to calculate.")

        # Round the total score for better readability
        total_score = round(total_score, 4)

        return jsonify({'total_score': total_score}), 200

    except Exception as e:
        # Add detailed error logging here
        import traceback
        error_details = traceback.format_exc()
        print("Error occurred:", error_details)
        return jsonify({'error': str(e), 'details': error_details}), 500
# @app.route('/api/recommendations', methods=['POST'])
# def get_player_recommendations():
#     data = request.json
#     user_id = data.get('userID')

#     if not user_id:
#         return jsonify({'error': 'UserID is required'}), 400

#     try:
#         # Fetch all players' stats for the user's roster
#         players_stats = Stats.query.all()  # This will get stats for all players, you might want to add filtering for roster players

#         # Define the scoring weights (same as before)
#         scoring_weights = {
#             'Completions': 0.5,
#             'PassingYards': 0.04,
#             'PassingTouchdowns': 4,
#             'Interceptions': -2,
#             'Sacks': -1,
#             'AdjQBR': 0.1,
#             'RushingYards': 0.1,
#             'RushingTouchdowns': 6,
#             'Receptions': 1,
#             'ReceivingYards': 0.1,
#             'ReceivingTouchdowns': 6,
#             'Fumbles': -1,
#             'FumblesLost': -1,
#             'FumblesRecovered': 1,
#             'TotalTackles': 1,
#             'PassesDefended': 2,
#             'DefensiveTouchdowns': 6,
#             'InterceptionYards': 0.1,
#             'InterceptionTouchdowns': 6,
#             'KickReturns': 0.5,
#             'KickReturnYards': 0.1,
#             'KickReturnTouchdowns': 6,
#             'PuntReturns': 0.5,
#             'PuntReturnYards': 0.1,
#             'PuntReturnTouchdowns': 6,
#             'FieldGoalsMade': 3,
#             'ExtraPointsMade': 1,
#             'TotalKickingPoints': 1,
#             'Punts': 0.1,
#             'PuntYards': 0.05,
#             'GrossAvgPuntYards': 0.05,
#             'Touchbacks': 1,
#             'PuntsInside20': 0.5,
#         }

#         player_scores = {}

#         # Calculate the total score for all players
#         for stat in players_stats:
#             player_id = stat.PlayerID
#             if player_id not in player_scores:
#                 player_scores[player_id] = {'total_score': 0, 'game_count': 0}

#             game_score = 0
#             for key, weight in scoring_weights.items():
#                 value = getattr(stat, key, None)
#                 value = value or 0
#                 game_score += value * weight

#             # Update total score and game count
#             player_scores[player_id]['total_score'] += game_score
#             player_scores[player_id]['game_count'] += 1

#         # Calculate average scores for each player
#         player_averages = []
#         for player_id, scores in player_scores.items():
#             if scores['game_count'] > 0:
#                 average_score = scores['total_score'] / scores['game_count']
#                 player_averages.append({'PlayerID': player_id, 'AverageScore': average_score})

#         # Sort players by average score in descending order
#         player_averages = sorted(player_averages, key=lambda x: x['AverageScore'], reverse=True)

#         return jsonify({'players': player_averages}), 200

#     except Exception as e:
#         import traceback
#         error_details = traceback.format_exc()
#         print("Error occurred:", error_details)
#         return jsonify({'error': str(e), 'details': error_details}), 500
@app.route('/api/recommendations', methods=['POST'])
def get_player_recommendations():
    data = request.json
    user_id = data.get('userID')

    if not user_id:
        return jsonify({'error': 'UserID is required'}), 400

    try:
        # Fetch the roster of players for the given user
        roster = Roster.query.filter(Roster.UserID == user_id).all()
        player_ids = [player.PlayerID for player in roster]

        # Fetch stats for only the players in the user's roster
        players_stats = Stats.query.filter(Stats.PlayerID.in_(player_ids)).all()

        # Define the scoring weights (same as before)
        scoring_weights = {
            'Completions': 0.5,
            'PassingYards': 0.04,
            'PassingTouchdowns': 4,
            'Interceptions': -2,
            'Sacks': -1,
            'AdjQBR': 0.1,
            'RushingYards': 0.1,
            'RushingTouchdowns': 6,
            'Receptions': 1,
            'ReceivingYards': 0.1,
            'ReceivingTouchdowns': 6,
            'Fumbles': -1,
            'FumblesLost': -1,
            'FumblesRecovered': 1,
            'TotalTackles': 1,
            'PassesDefended': 2,
            'DefensiveTouchdowns': 6,
            # 'InterceptionsDefensive': 2,
            'InterceptionYards': 0.1,
            'InterceptionTouchdowns': 6,
            'KickReturns': 0.5,
            'KickReturnYards': 0.1,
            'KickReturnTouchdowns': 6,
            'PuntReturns': 0.5,
            'PuntReturnYards': 0.1,
            'PuntReturnTouchdowns': 6,
            'FieldGoalsMade': 3,
            'ExtraPointsMade': 1,
            'TotalKickingPoints': 1,
            'Punts': 0.1,
            'PuntYards': 0.05,
            'GrossAvgPuntYards': 0.05,
            'Touchbacks': 1,
            'PuntsInside20': 0.5,
        }

        player_scores = {}

        # Calculate the total score for each player
        for stat in players_stats:
            player_id = stat.PlayerID
            if player_id not in player_scores:
                player_scores[player_id] = {'total_score': 0, 'game_count': 0}

            game_score = 0
            for key, weight in scoring_weights.items():
                value = getattr(stat, key, None)
                value = value or 0
                game_score += value * weight

            # Update total score and game count
            player_scores[player_id]['total_score'] += game_score
            player_scores[player_id]['game_count'] += 1

        # Calculate average scores for each player
        player_averages = []
        for player_id, scores in player_scores.items():
            if scores['game_count'] > 0:
                average_score = scores['total_score'] / scores['game_count']
                player_averages.append({'PlayerID': player_id, 'AverageScore': average_score})

        # Sort players by average score in descending order
        player_averages = sorted(player_averages, key=lambda x: x['AverageScore'], reverse=True)

        return jsonify({'players': player_averages}), 200

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print("Error occurred:", error_details)
        return jsonify({'error': str(e), 'details': error_details}), 500




if __name__ == '__main__':
    app.run(debug=True)