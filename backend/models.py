from app import db


# class Player(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), nullable=False)
#     team = db.Column(db.String(50), nullable=False)
#     position = db.Column(db.String(20), nullable=False)
#     # points = db.Column(db.Float, default=0.0)


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
class League(db.Model):
    __tablename__ = 'league'

    LeagueID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Week = db.Column(db.String(10), nullable=False)  # Week identifier (e.g., 'Week 1', 'Week 2')
    User1ID = db.Column(db.Integer, db.ForeignKey('user.UserID'), nullable=False)
    User2ID = db.Column(db.Integer, db.ForeignKey('user.UserID'), nullable=False)
    User1_Score = db.Column(db.Integer, nullable=False)
    User2_Score = db.Column(db.Integer, nullable=False)

    # Relationships
    user1 = db.relationship('User', foreign_keys=[User1ID], backref=db.backref('user1_matches', lazy=True))
    user2 = db.relationship('User', foreign_keys=[User2ID], backref=db.backref('user2_matches', lazy=True))
    
    def __repr__(self):
        return f"<League Week={self.Week} User1ID={self.User1ID} User2ID={self.User2ID}>"



class InjuryReports(db.Model):
    __tablename__ = 'injuryreports'

    ReportID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    PlayerID = db.Column(db.Integer, db.ForeignKey('player.PlayerID'), nullable=False)
    InjuryType = db.Column(db.String(100), nullable=False)
    StartDate = db.Column(db.Date, nullable=True)
    ExpectedReturnDate = db.Column(db.Date, nullable=True)
    CurrentStatus = db.Column(db.String(50), nullable=True)

    # Relationship to Player
    player = db.relationship('Player', backref=db.backref('injury_reports', lazy=True))


class WeeklyChallenges(db.Model):
    __tablename__ = 'weeklychallenges'

    ChallengeID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Description = db.Column(db.Text, nullable=False)
    PointsAwarded = db.Column(db.Integer, nullable=False)
    ChallengeDate = db.Column(db.Date, nullable=True)


class UserChallenges(db.Model):
    __tablename__ = 'userchallenges'

    UserChallengeID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'), nullable=False)
    ChallengeID = db.Column(db.Integer, db.ForeignKey('weeklychallenges.ChallengeID'), nullable=False)
    CompletionStatus = db.Column(db.Boolean, default=False)

    # Relationships
    user = db.relationship('User', backref=db.backref('user_challenges', lazy=True))
    challenge = db.relationship('WeeklyChallenges', backref=db.backref('user_challenges', lazy=True))


class GameWeek(db.Model):
    __tablename__ = 'gameweek'

    GameWeekID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    UserID = db.Column(db.Integer, db.ForeignKey('user.UserID'), nullable=False)
    PlayerID = db.Column(db.Integer, db.ForeignKey('player.PlayerID'), nullable=False)
    Scores = db.Column(db.JSON, nullable=True)
    ChallengeBonusPoints = db.Column(db.Integer, default=0)

    # Relationships
    user = db.relationship('User', backref=db.backref('game_weeks', lazy=True))
    player = db.relationship('Player', backref=db.backref('game_weeks', lazy=True))
    DateOfMatch = db.Column(db.Date, nullable=True)  # Add DateOfMatch column to store match date
    
    @property
    def week_number(self):
        if self.DateOfMatch:
            return self.DateOfMatch.isocalendar()[1]
        return None


class HeadToHead(db.Model):
    __tablename__ = 'headtohead'

    MatchupID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    User1ID = db.Column(db.Integer, db.ForeignKey('user.UserID'), nullable=False)
    User2ID = db.Column(db.Integer, db.ForeignKey('user.UserID'), nullable=False)
    WinnerID = db.Column(db.Integer, db.ForeignKey('user.UserID'), nullable=True)
    DateOfMatch = db.Column(db.Date, nullable=True)

    # Relationships
    user1 = db.relationship('User', foreign_keys=[User1ID], backref=db.backref('matches_as_user1', lazy=True))
    user2 = db.relationship('User', foreign_keys=[User2ID], backref=db.backref('matches_as_user2', lazy=True))
    winner = db.relationship('User', foreign_keys=[WinnerID], backref=db.backref('matches_won', lazy=True))
