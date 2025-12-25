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
matches["Targert"]  = (matches["Result"] == "W").astype("int")
rf = RandomForestClassifier(n_estimators=50,min_samples_split=10,random_state=1)
train = matches[matches["Date"] < '2025-01-01']
test = matches[matches["Date"] > '2025-01-01']
predictors = ["Vnue_Code", "Opp_Code", "Hour", "Day_Code"]
rf.fit(train[predictors], train["Targert"])
pre = rf.predict(test[predictors])
acc = accuracy_score(test["Targert"], pre)
combined = pd.DataFrame(dict(actual=test["Targert"], predicted=pre))
pd.crosstab(index=combined["actual"], columns=combined["predicted"])
print(pd.crosstab(index=combined["actual"], columns=combined["predicted"]))
print(acc)
print(precision_score(test["Targert"], pre))
group_matches= matches.groupby("team")
group = group_matches.get_group("Arsenal")
def roll (group , cols , new_cols):
    group = group.sort_values("Date")
    roll_stat = group[cols].rolling(3,closed= 'left').mean()
    group[new_cols] = roll_stat
    group = group.dropna(subset=new_cols)
    return group
cols = ["GF","GA","Sh", "SoT", "Dist", "FK", "PK", "PKatt"]
new_cols = [f"{c}_rolling" for c in cols]
group = roll(group, cols, new_cols)
matches_roll = matches.groupby("team").apply(lambda x: roll(x, cols, new_cols))
matches_roll = matches_roll.droplevel('team')
matches_roll.index = range(matches_roll.shape[0])
print(matches_roll)
