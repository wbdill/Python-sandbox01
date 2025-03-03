import pandas as pd

df = pd.read_csv("input/Census_county_race_2020.csv")

df.loc[0:5, 'total_pop']
df.iloc[0:5, 0:9]
df[df['state'].isin(['TN'])]
df[df['state'].isin(['TN']) & df['county'].isin(['Williamson County', 'Davidson County'])]

df.groupby('state').agg({'total_pop': ['mean', 'sum']})


#df['total_pop']
df.describe()


