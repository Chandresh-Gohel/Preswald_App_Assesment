from preswald import connect, get_df

connect()  # Initialize connection to preswald.toml data sources
df = get_df("my_dataset")  # Load data

from preswald import query

df['Age'] = df['Age'].astype(int)  
filtered_df = df[df['Age'] > 20]

from preswald import table, text

text("# Social Media Addiction Analysis App")
table(filtered_df, title="Filtered Data")

from preswald import plotly
import plotly.express as px

fig = px.scatter(df, x="Mental_Health_Score", 
y="Avg_Daily_Usage_Hours", 
color="Most_Used_Platform")
plotly(fig)
