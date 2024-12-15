import mysql.connector
import pandas as pd

# Establish the connection to MySQL
db_connection = mysql.connector.connect(
    host="localhost",         # or your MySQL host
    user="root",     # your MySQL username
    password="root1234", # your MySQL password
    database="FINAL_NFL_STATS"
)

# Load your cleaned CSV file into a DataFrame
csv_file = '/Users/marcojonsson/FantasyFootball/fantasy2/fantasyfootball/SOURCEDATA/nfl_clean_stats.csv'
df = pd.read_csv(csv_file)

# Prepare the cursor to interact with the database
cursor = db_connection.cursor()
count = 0

# Loop through each row in the DataFrame and insert data into the table

# IF error insert InterceptionsDefensive = VALUES(InterceptionsDefensive), between defensive td and interception yards
for index, row in df.iterrows():
    count+=1
    print("Records Inserted: ", count)
    insert_query = """
    INSERT INTO STATS (
        GameID, PlayerID, PlayerName, TeamAB, Position, StatType,
        PassingYards, YardsPerPassAttempt, PassingTouchdowns, Interceptions, 
        AdjQBR, QBRating, RushingAttempts, RushingYards, 
        YardsPerRushAttempt, RushingTouchdowns, LongRushing, Receptions, 
        ReceivingYards, YardsPerReception, ReceivingTouchdowns, LongReception, 
        ReceivingTargets, Fumbles, FumblesLost, FumblesRecovered, TotalTackles, 
        SoloTackles, Sacks, TacklesForLoss, PassesDefended, QBHits, DefensiveTouchdowns, 
        InterceptionYards, InterceptionTouchdowns, KickReturns, 
        KickReturnYards, YardsPerKickReturn, LongKickReturn, KickReturnTouchdowns, 
        PuntReturns, PuntReturnYards, YardsPerPuntReturn, LongPuntReturn, PuntReturnTouchdowns, 
        FieldGoalsMade, FieldGoalPct, LongFieldGoalMade, 
        ExtraPointsMade, TotalKickingPoints, Punts, PuntYards, 
        GrossAvgPuntYards, Touchbacks, PuntsInside20, LongPunt, Completions, Week
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE 
    PassingYards = VALUES(PassingYards),
    YardsPerPassAttempt = VALUES(YardsPerPassAttempt),
    PassingTouchdowns = VALUES(PassingTouchdowns),
    Interceptions = VALUES(Interceptions),
    AdjQBR = VALUES(AdjQBR),
    QBRating = VALUES(QBRating),
    RushingAttempts = VALUES(RushingAttempts),
    RushingYards = VALUES(RushingYards),
    YardsPerRushAttempt = VALUES(YardsPerRushAttempt),
    RushingTouchdowns = VALUES(RushingTouchdowns),
    LongRushing = VALUES(LongRushing),
    Receptions = VALUES(Receptions),
    ReceivingYards = VALUES(ReceivingYards),
    YardsPerReception = VALUES(YardsPerReception),
    ReceivingTouchdowns = VALUES(ReceivingTouchdowns),
    LongReception = VALUES(LongReception),
    ReceivingTargets = VALUES(ReceivingTargets),
    Fumbles = VALUES(Fumbles),
    FumblesLost = VALUES(FumblesLost),
    FumblesRecovered = VALUES(FumblesRecovered),
    TotalTackles = VALUES(TotalTackles),
    SoloTackles = VALUES(SoloTackles),
    Sacks = VALUES(Sacks),
    TacklesForLoss = VALUES(TacklesForLoss),
    PassesDefended = VALUES(PassesDefended),
    QBHits = VALUES(QBHits),
    DefensiveTouchdowns = VALUES(DefensiveTouchdowns),
    InterceptionYards = VALUES(InterceptionYards),
    InterceptionTouchdowns = VALUES(InterceptionTouchdowns),
    KickReturns = VALUES(KickReturns),
    KickReturnYards = VALUES(KickReturnYards),
    YardsPerKickReturn = VALUES(YardsPerKickReturn),
    LongKickReturn = VALUES(LongKickReturn),
    KickReturnTouchdowns = VALUES(KickReturnTouchdowns),
    PuntReturns = VALUES(PuntReturns),
    PuntReturnYards = VALUES(PuntReturnYards),
    YardsPerPuntReturn = VALUES(YardsPerPuntReturn),
    LongPuntReturn = VALUES(LongPuntReturn),
    PuntReturnTouchdowns = VALUES(PuntReturnTouchdowns),
    FieldGoalsMade = VALUES(FieldGoalsMade),
    FieldGoalPct = VALUES(FieldGoalPct),
    LongFieldGoalMade = VALUES(LongFieldGoalMade),
    ExtraPointsMade = VALUES(ExtraPointsMade),
    TotalKickingPoints = VALUES(TotalKickingPoints),
    Punts = VALUES(Punts),
    PuntYards = VALUES(PuntYards),
    GrossAvgPuntYards = VALUES(GrossAvgPuntYards),
    Touchbacks = VALUES(Touchbacks),
    PuntsInside20 = VALUES(PuntsInside20),
    LongPunt = VALUES(LongPunt),
    Completions = VALUES(Completions),
    PlayerID = VALUES(PlayerID)
    """
    # Check the number of placeholders
    # print(f"Placeholders count: {insert_query.count('%s')}")


    # Prepare the data to insert into the query
    data = (
        row['GameID'], row['PlayerID'], row['PlayerName'], row['Team'], row['Position'], row['StatType'],
        row['passingYards'], row['yardsPerPassAttempt'], row['passingTouchdowns'], row['interceptions'],
        row['adjQBR'], row['QBRating'], row['rushingAttempts'], row['rushingYards'],
        row['yardsPerRushAttempt'], row['rushingTouchdowns'], row['longRushing'], row['receptions'], row['receivingYards'],
        row['yardsPerReception'], row['receivingTouchdowns'], row['longReception'], row['receivingTargets'], 
        row['fumbles'], row['fumblesLost'], row['fumblesRecovered'], row['totalTackles'], row['soloTackles'], row['sacks'], 
        row['tacklesForLoss'], row['passesDefended'], row['QBHits'], row['defensiveTouchdowns'],
        row['interceptionYards'], row['interceptionTouchdowns'], row['kickReturns'], row['kickReturnYards'], row['yardsPerKickReturn'],
        row['longKickReturn'], row['kickReturnTouchdowns'], row['puntReturns'], row['puntReturnYards'], row['yardsPerPuntReturn'],
        row['longPuntReturn'], row['puntReturnTouchdowns'], row['fieldGoalsMade'], row['fieldGoalPct'],
        row['longFieldGoalMade'], row['extraPointsMade'], row['totalKickingPoints'], row['punts'],
        row['puntYards'], row['grossAvgPuntYards'], row['touchbacks'], row['puntsInside20'], row['longPunt'], row['completions'], row['Week']
    )
    # print(f"Data: {data}")
    # print(f"Data length: {len(data)}")
    # print(df.columns)


    # Execute the query
    # print(f"Inserting data for Player: {row['PlayerName']}, Team: {row['Team']}")
    # print(f"Data: {data}")
    # print(f"Data length: {len(data)}")
    # print(f"Placeholders count: {insert_query.count('%s')}")

    cursor.execute(insert_query, data)

# Commit the transaction to save data
db_connection.commit()

# Close the cursor and the connection
cursor.close()
db_connection.close()

print("Data has been successfully uploaded into the STATS table!")
