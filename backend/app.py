from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import text  # Import for raw SQL queries
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root1234@localhost/test'
db = SQLAlchemy(app)

def row_to_dict(row):
    """Convert SQLAlchemy Row to dictionary using _mapping."""
    return dict(row._mapping)  # Use _mapping to access row data

@app.route('/api/players', methods=['GET'])
def get_players():
    try:
        with db.engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM players;"))
            data = [row_to_dict(row) for row in result]
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

migrate = Migrate(app, db)

@app.route('/')
def home():
    return "Welcome to the Fantasy Football API with MySQL!"

@app.route('/test-connection')
def test_connection():
    try:
        with db.engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM players;"))
            data = [row_to_dict(row) for row in result]
            return {"status": "success", "data": data}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True)
