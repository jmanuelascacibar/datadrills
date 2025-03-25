# Find the monthly retention rate of users for each activity account separately for December 2020 and January 2021

#  The retention rate is defined as the percentage of users active in a given month who have activity in any future month.

import pandas as pd
import numpy as np

df = sf_events 

# Convert the record_date column to datetime format
df["record_date"] = pd.to_datetime(df["record_date"], format="%Y-%m-%d")

# Filter December 2020 data
# Remove duplicates 
# The objective is to find unique users who were active in a particular month and not how many times each user was active. Without removing duplicates a single user who performed multiple activities would be counted multiple times.
dec_2020 = df[
    (df["record_date"].dt.year == 2020) & (df["record_date"].dt.month == 12)
    ][["account_id", "user_id"]].drop_duplicates()
    
jan_2021 = df[
    (df["record_date"].dt.year== 2021) & (df["record_date"].dt.month == 1)
    ][["account_id", "user_id"]].drop_duplicates()
    
# Find the last activity date for each user
user_last_act = df.groupby("user_id")["record_date"].max().to_frame("last_date").reset_index()
    
# Merge last activity to dec_2020 and jan_2021
dec_2020 = pd.merge(dec_2020, user_last_act, on="user_id")
jan_2021 = pd.merge(jan_2021, user_last_act, on="user_id")

# Initialize retention col
dec_2020["retention"] = 0
jan_2021["retention"] = 0

# Setting retention for Dec and Jan users
dec_2020.loc[dec_2020["last_date"] > "2020-12-31", "retention"] = 1
jan_2021.loc[jan_2021["last_date"] > "2021-01-31", "retention"] = 1

# Calculate retention rate
ret_dec2020 = dec_2020.groupby("account_id")["retention"].mean().to_frame("dec_retention_rate").reset_index()

ret_jan2021 = jan_2021.groupby("account_id")["retention"].mean().to_frame("jan_retention_rate").reset_index()

# Merge retention rates in a single dataframe
merged = ret_dec2020.merge(ret_jan2021, on="account_id")

# Calculate the ratio
merged["retention"] = np.where(
    merged["dec_retention_rate"] > 0,
    merged["jan_retention_rate"] / merged["dec_retention_rate"],
    0
)
# Final output
merged[["account_id", "retention"]]
