import pandas as pd
df = facebook_web_log

df["date"] = df.timestamp.dt.date

# Filter the df by page_load and page_exit
loads = df[df.action == "page_load"].copy()
exits = df[df.action == "page_exit"].copy()

# Get the latest page_load and the earliest page_exit by user and date
latest_loads = loads.groupby(["user_id", "date"])["timestamp"].max().reset_index()
latest_loads.rename(columns={'timestamp': 'load_time'}, inplace=True)
earliest_exits = exits.groupby(["user_id", "date"])["timestamp"].min().reset_index()
earliest_exits.rename(columns={'timestamp': 'exit_time'}, inplace=True)
# Merge data
sessions = pd.merge(latest_loads, earliest_exits, on=["user_id", "date"], how="inner")
# Filter out invalid sessions
sessions = sessions[sessions.load_time < sessions.exit_time]

# Calculate session duration
sessions["session_duration"] = (sessions.exit_time - sessions.load_time).dt.total_seconds()

# Calculate user average session time
avg_sessions = sessions.groupby("user_id")["session_duration"].mean().reset_index()

avg_sessions.rename(columns={"session_duration": "avg_session_time"}, inplace = True)

# Expected output pandas dataframe 2D 
avg_sessions[["user_id", "avg_session_time"]]
