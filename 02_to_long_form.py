import pandas as pd

df = pd.read_csv('elections.csv')

candidate = df.groupby(['year', 'party']).candidate.agg(lambda x: x.value_counts().index[0]).reset_index()
candidate.to_csv('output/candidates.csv', index=False)
del candidate

df = df[['year', 'short_state', 'votes', 'party']]

df['party'] = df['party'].apply(lambda x: x if x in ['Democratic', 'Republican'] else 'Other')

df_reshape = df.pivot_table(index=['year', 'short_state'] , columns='party', values='votes')
df_reshape = df_reshape.reset_index().fillna(0)
df_reshape[['Democratic', 'Republican', 'Other']] = df_reshape[['Democratic', 'Republican', 'Other']].astype(int)
print(df_reshape)

df_reshape.rename(columns={
    'short_state': 'State',
    'Democratic': 'Democrat',
    'year': 'Year'
}, inplace=True)

print(df_reshape.columns)

df_reshape[['State', 'Democrat', 'Republican', 'Other', 'Year']].to_csv('output/election.csv', index=False)
