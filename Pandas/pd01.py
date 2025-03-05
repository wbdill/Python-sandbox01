import pandas as pd
help(pd.read_csv)
df = pd.read_csv("input/Census_county_race_2020.csv")

df.loc[0:5, 'total_pop']
df.iloc[0:5, 0:9]
df[df['state'].isin(['TN'])]
df[df['state'].isin(['TN']) & df['county'].isin(['Williamson County', 'Davidson County'])]
help(pd.read_csv)
df.groupby('state').agg({'total_pop': ['mean', 'sum', 'min', 'max']})
df.nlargest(5, 'total_pop')
df.explode('total_pop')

# select count(*) AS N group by state ORDER BY N DESC
df['state'].value_counts() #  normalize=True gives pct of total

# counties that exist in 15 or more states
df['county'].value_counts()[df['county'].value_counts() >= 15]

# all counties that contain "Williamson"
df[df['county'].str.contains("Williamson")]


#df['total_pop']
df.describe()


