from preswald import connect, get_df, table, text, plotly, select, slider
import plotly.express as px
import pandas as pd

# Connect to data source specified in preswald.toml
connect()
df = get_df("social_data")  # This name must match the one in [data.social_data] in preswald.toml

# Ensure numeric data types for accurate filtering and plotting
df['Age'] = df['Age'].astype(int)
df['Mental_Health_Score'] = df['Mental_Health_Score'].astype(float)

# Add filter controls to the UI
gender = select("Gender", df["Gender"].dropna().unique().tolist(), default="Female")  # Dropdown to filter by gender
min_age = slider("Min Age", min=10, max=60, step=1, default=18)  # Slider to set minimum age
min_mental = slider("Mental Health Score ≥", min=0, max=10, step=1, default=5)  # Slider to filter by mental health score

# Filter the dataframe based on user input
filtered_df = df[
    (df["Gender"] == gender) &
    (df["Age"] >= min_age) &
    (df["Mental_Health_Score"] >= min_mental)
]

# Title text displayed on top of the UI
text("# Social Media & Mental Health Dashboard")

# Display the filtered data as a table in the app
table(filtered_df, title="Filtered Data")

# Create and display a scatterplot showing relationship between usage hours and mental health score
fig1 = px.scatter(
    filtered_df,
    x="Avg_Daily_Usage_Hours",
    y="Mental_Health_Score",
    color="Most_Used_Platform",
    title="Daily Usage vs. Mental Health Score"
)
plotly(fig1)

# Group ages into buckets for grouped analysis
bins = [10, 20, 30, 40, 50, 60]
labels = ['10–19', '20–29', '30–39', '40–49', '50–59']
df["Age_Group"] = pd.cut(df["Age"], bins=bins, labels=labels, right=False)

# Compute average mental health score per age group
grouped = (
    df.groupby("Age_Group")["Mental_Health_Score"]
    .mean()
    .reset_index()
    .dropna()
)

# Display a bar chart showing average mental health score by age group
fig2 = px.bar(
    grouped,
    x="Age_Group",
    y="Mental_Health_Score",
    title="Average Mental Health Score by Age Group",
    labels={"Mental_Health_Score": "Avg Score"}
)
plotly(fig2)

# Count users per social media platform
platform_counts = (
    df["Most_Used_Platform"]
    .value_counts()
    .reset_index()
    .rename(columns={"index": "Platform", "Most_Used_Platform": "Users"})
)

# Display a pie chart of platform usage distribution
fig3 = px.pie(
    platform_counts,
    names="Platform",
    values="Users",
    title="Distribution of Most Used Social Media Platforms"
)
plotly(fig3)
