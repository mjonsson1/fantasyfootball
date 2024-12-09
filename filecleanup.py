import pandas as pd
import numpy as np

# Load the CSV file
input_csv = '/Users/marcojonsson/FantasyFootball/fantasyfootball/SOURCEDATA/nfl_player_stats.csv'
output_csv = 'nfl_clean_stats.csv'

# Define the function to process 'X/Y' type entries
def process_raw_value(value):
    if isinstance(value, str) and '/' in value:
        try:
            numerator, _ = value.split('/')  # Ignore the denominator
            return int(numerator)  # Return the raw successful attempts
        except ValueError:
            return 0  # In case of malformed data
    try:
        return float(value)  # If it's already a number
    except ValueError:
        return 0  # In case of missing or invalid data

# Define a function to process 'X-Y' type entries
def process_dash_value(value):
    if isinstance(value, str) and '-' in value:
        try:
            numerator, _ = value.split('-')  # Ignore the second part
            return int(numerator)  # Return the first value (e.g., sacks)
        except ValueError:
            return 0  # In case of malformed data
    try:
        return float(value)  # If it's already a number
    except ValueError:
        return 0  # In case of missing or invalid data

def truncate_percentages(value):
    try:
        # Try converting value to float
        num = float(value)
        # Truncate to 1 decimal place
        return np.trunc(num * 10) / 10
    except (ValueError, TypeError):
        return 0  # In case of invalid data or non-numeric values

# Custom aggregation function for mean, excluding zero values
def mean_excluding_zeros(values):
    non_zero_values = [v for v in values if v != 0]
    if non_zero_values:
        return np.mean(non_zero_values)
    else:
        return 0  # If all values are zero, return zero

# Load the data into a pandas DataFrame
df = pd.read_csv(input_csv)

# Remove rows where PlayerID is negative or "team" (string "team" in PlayerID)
df = df[~df['PlayerID'].isin(['team'])]  # Remove rows where PlayerID is "team"
df = df[df['PlayerID'] >= 0]  # Remove rows where PlayerID is negative

# Process 'completions/passingAttempts' column
if 'completions/passingAttempts' in df.columns:
    df['completions'] = df['completions/passingAttempts'].apply(process_raw_value)
    df.drop(columns=['completions/passingAttempts'], inplace=True)
if 'fieldGoalsMade/fieldGoalAttempts' in df.columns:
    df['fieldGoalsMade'] = df['fieldGoalsMade/fieldGoalAttempts'].apply(process_raw_value)
    df.drop(columns=['fieldGoalsMade/fieldGoalAttempts'], inplace=True)
if 'extraPointsMade/extraPointAttempts' in df.columns:
    df['extraPointsMade'] = df['extraPointsMade/extraPointAttempts'].apply(process_raw_value)
    df.drop(columns=['extraPointsMade/extraPointAttempts'], inplace=True)
# Process 'sacks-sackYardsLost' column
if 'sacks-sackYardsLost' in df.columns:
    df['sacks'] = df['sacks-sackYardsLost'].apply(process_dash_value)
    df.drop(columns=['sacks-sackYardsLost'], inplace=True)
if 'adjQBR' in df.columns:
    df['adjQBR'] = df['adjQBR'].apply(truncate_percentages)

# List of all columns to keep, including PlayerName, Team, Position, StatType, etc.
all_columns = [
    'GameID', 'PlayerID', 'PlayerName', 'Team', 'Position', 'StatType',
    'passingYards', 'yardsPerPassAttempt', 'passingTouchdowns', 'interceptions',
    'adjQBR', 'QBRating', 'rushingAttempts', 'rushingYards',
    'yardsPerRushAttempt', 'rushingTouchdowns', 'longRushing', 'receptions', 'receivingYards',
    'yardsPerReception', 'receivingTouchdowns', 'longReception', 'receivingTargets', 
    'fumbles', 'fumblesLost', 'fumblesRecovered', 'totalTackles', 'soloTackles', 'sacks', 
    'tacklesForLoss', 'passesDefended', 'QBHits', 'defensiveTouchdowns', 'interceptions.1',
    'interceptionYards', 'interceptionTouchdowns', 'kickReturns', 'kickReturnYards', 'yardsPerKickReturn',
    'longKickReturn', 'kickReturnTouchdowns', 'puntReturns', 'puntReturnYards', 'yardsPerPuntReturn',
    'longPuntReturn', 'puntReturnTouchdowns', 'fieldGoalsMade', 'fieldGoalPct',
    'longFieldGoalMade', 'extraPointsMade', 'totalKickingPoints', 'punts',
    'puntYards', 'grossAvgPuntYards', 'touchbacks', 'puntsInside20', 'longPunt', 'completions'
]

# Aggregation rules
aggregation_rules = {
    'PlayerName': 'first',  # Keep the first occurrence for PlayerName
    'Team': 'first',        # Keep the first occurrence for Team
    'Position': 'first',    # Keep the first occurrence for Position
    'StatType': 'first',    # Keep the first occurrence for StatType
    'passingYards': 'sum',
    'yardsPerPassAttempt': 'mean',
    'passingTouchdowns': 'sum',
    'interceptions': 'sum',
    'adjQBR': mean_excluding_zeros,
    'QBRating': mean_excluding_zeros,
    'rushingAttempts': 'sum',
    'rushingYards': 'sum',
    'yardsPerRushAttempt': 'mean',
    'rushingTouchdowns': 'sum',
    'longRushing': 'first',
    'receptions': 'sum',
    'receivingYards': 'sum',
    'yardsPerReception': 'mean',
    'receivingTouchdowns': 'sum',
    'longReception': 'first',
    'receivingTargets': 'sum',
    'fumbles': 'sum',
    'fumblesLost': 'sum',
    'fumblesRecovered': 'sum',
    'totalTackles': 'sum',
    'soloTackles': 'sum',
    'sacks': 'sum',
    'tacklesForLoss': 'sum',
    'passesDefended': 'sum',
    'QBHits': 'sum',
    'defensiveTouchdowns': 'sum',
    'interceptions.1': 'sum',
    'interceptionYards': 'sum',
    'interceptionTouchdowns': 'sum',
    'kickReturns': 'sum',
    'kickReturnYards': 'sum',
    'yardsPerKickReturn': 'mean',
    'longKickReturn': 'first',
    'kickReturnTouchdowns': 'sum',
    'puntReturns': 'sum',
    'puntReturnYards': 'sum',
    'yardsPerPuntReturn': 'mean',
    'longPuntReturn': 'first',
    'puntReturnTouchdowns': 'sum',
    'fieldGoalsMade': 'sum',
    'fieldGoalPct': 'mean',
    'longFieldGoalMade': 'first',
    'extraPointsMade': 'sum',
    'totalKickingPoints': 'sum',
    'punts': 'sum',
    'puntYards': 'sum',
    'grossAvgPuntYards': 'mean',
    'touchbacks': 'sum',
    'puntsInside20': 'sum',
    'longPunt': 'first',
    'completions': 'sum'
}

# Group by GameID and PlayerID and apply the aggregation rules
df_aggregated = df.groupby(['GameID', 'PlayerID'], as_index=False).agg(aggregation_rules)

# Save the cleaned and aggregated DataFrame to a new CSV
df_aggregated.to_csv(output_csv, index=False)

print(f"Cleaned and aggregated data saved to {output_csv}")
