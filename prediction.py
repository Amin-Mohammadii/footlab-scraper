import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
matches = pd.read_csv('matches.csv')
matches["Date"] = pd.to_datetime(matches["Date"])
matches["Vnue_Code"] = matches["Venue"].astype("category").cat.codes
matches["Opp_Code"] = matches["Opponent"].astype("category").cat.codes
matches["Hour"] = matches["Time"].str.replace(":.+", "", regex=True).astype("int")
matches["Day_Code"] = matches["Date"].dt.dayofweek
matches["Target"]  = (matches["Result"] == "W").astype("int")
rf = RandomForestClassifier(n_estimators=500,min_samples_split=500,random_state=1)
train = matches[matches["Date"] < '2025-01-01']
test = matches[matches["Date"] > '2025-01-01']
predictors = ["Vnue_Code", "Opp_Code", "Hour", "Day_Code"]
rf.fit(train[predictors], train["Target"])
preds = rf.predict(test[predictors])
acc = accuracy_score(test["Target"], preds)
print(acc)
print(precision_score(test["Target"], preds))

group_matches= matches.groupby("team")
group = group_matches.get_group("Arsenal")
def roll (group , cols , new_cols):
    group = group.sort_values("Date")
    rolling_stats = group[cols].rolling(3,closed= 'left').mean()
    group[new_cols] = rolling_stats
    group = group.dropna(subset=new_cols)
    return group
cols = ["GF","GA","Sh", "SoT", "Dist", "FK", "PK", "PKatt"]
new_cols = [f"{c}_rolling" for c in cols]
group = roll(group, cols, new_cols)
matches_roll = matches.groupby("team").apply(lambda x: roll(x, cols, new_cols))
matches_roll = matches_roll.droplevel('team')
matches_roll.index = range(matches_roll.shape[0])

def make_predictions(matches , predictors ):
    train = matches[matches["Date"] < '2025-01-01']
    test = matches[matches["Date"] > '2025-01-01']
    rf.fit(train[predictors], train["Target"])
    preds = rf.predict(test[predictors])
    combined = pd.DataFrame(dict(actual=test["Target"], predicted=preds), index=test.index)
    P= precision_score(test["Target"], preds)
    return combined, P
combined,P = make_predictions(matches_roll,predictors + new_cols)
print(P)
print (matches_roll.columns)
combined = combined.merge(matches_roll[["Date", "team","Opponent", "Result"]], left_index=True, right_index=True)
print(combined)




class MissingDict(dict):
    __missing__ = lambda self, key: key

map_values = {

    "Brighton and Hove Albion": "Brighton",
    "Manchester United": "Manchester Utd",
    "Newcastle United": "Newcastle Utd",
    "Tottenham Hotspur": "Tottenham",
    "West Ham United": "West Ham",
    "Wolverhampton Wanderers": "Wolves"
}
mapping = MissingDict(**map_values)
combined["new_team"] = combined["team"].map(mapping)
merged = combined.merge(combined, left_on=["Date", "new_team"], right_on=["Date", "Opponent"])
print(merged[(merged["predicted_x"] == 1) & (merged["predicted_y"] ==0)]["actual_x"].value_counts()
)
print(merged)