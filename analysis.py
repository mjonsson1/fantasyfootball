import pandas as pd

# Define your scoring weights for each stat (these are sample weights, adjust as needed)
scoring_weights = {
    'completions': 0.5,
    'passingYards': 0.04,
    'passingTouchdowns': 4,
    'interceptions': -2,
    'sacks': -1,
    'adjQBR': 0.1,
    'rushingYards': 0.1,
    'rushingTouchdowns': 6,
    'receptions': 1,
    'receivingYards': 0.1,
    'receivingTouchdowns': 6,
    'fumbles': -1,
    'fumblesLost': -1,
    'fumblesRecovered': 1,
    'totalTackles': 1,
    'sacks': 3,
    'passesDefended': 2,
    'defensiveTouchdowns': 6,
    'interceptions': 2,
    'interceptionYards':0.1,
    'interceptionTouchdowns':6,
    'kickReturns': 0.5,
    'kickReturnYards': 0.1,
    'kickReturnTouchdowns': 6,
    'puntReturns': 0.5,
    'puntReturnYards': 0.1,
    'puntReturnTouchdowns': 6,
    'fieldGoalsMade/fieldGoalAttempts': 3,
    'fieldGoalPct': 0.05,
    'extraPointsMade/extraPointAttempts': 1,
    'totalKickingPoints': 1,
    'punts': 0.1,
    'puntYards': 0.05,
    'grossAvgPuntYards': 0.05,
    'touchbacks': 1,
    'puntsInside20': 0.5,
}

# Function to process '2/2' type entries and return only the raw value (successful attempts)
def process_raw_value(value):
    if isinstance(value, str) and '/' in value:
        try:
            numerator, _ = value.split('/')  # Ignore the denominator
            return float(numerator)  # Return the raw successful attempts
        except ValueError:
            return 0  # In case of malformed data
    try:
        return float(value)  # If it's already a number
    except ValueError:
        return 0  # In case of missing or invalid data

# Function to calculate player contribution score
def calculate_score(player_stats, weights):
    score = 0
    for stat, weight in weights.items():
        if stat in player_stats:
            raw_value = process_raw_value(player_stats[stat])  # Get the raw value
            if pd.notna(raw_value):  # If valid raw count
                score += raw_value * weight
    return score

# Load CSV file into DataFrame
def load_player_data(csv_file):
    try:
        df = pd.read_csv(csv_file)
        print(f"Loaded data with {len(df)} rows and {len(df.columns)} columns.")
        return df
    except FileNotFoundError:
        print(f"Error: The file at {csv_file} was not found.")
        return None

# Function to get the highest scoring player by position
def get_top_players_by_position(df, weights):
    if df is not None:
        # Ensure there's no missing or incorrect columns
        missing_columns = [col for col in weights if col not in df.columns]
        if missing_columns:
            print(f"Warning: The following columns are missing from the CSV: {missing_columns}")
        
        # Calculate scores
        df['score'] = df.apply(lambda row: calculate_score(row, weights), axis=1)
        
        # Find the top scorer by position
        top_players = df.loc[df.groupby('Position')['score'].idxmax()]
        
        return top_players[['PlayerName', 'Position', 'score']]
    return None

# Example usage
csv_file = '/Users/marcojonsson/FantasyFootball/fantasyfootball/SOURCEDATA/nfl_clean_stats.csv'  # Replace with the path to your CSV file
df = load_player_data(csv_file)
top_players = get_top_players_by_position(df, scoring_weights)

# Print the results
if top_players is not None:
    print(top_players)
