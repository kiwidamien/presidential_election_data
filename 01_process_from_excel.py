import pandas as pd
import numpy as np

def import_election_sheet(filename = 'input/elections.xlsx'):
    # This is inspired by the post
    # https://stackoverflow.com/questions/41251922/error-when-using-pandas-read-excelheader-0-1
    # which shows how to import multi-index headers, if some of the cells are merged.

    df = pd.read_excel(filename, header = None)

    # drop nationwide
    df.drop(2, inplace=True)

    values = df.values
    # make a multiindex from the first two rows, starting at column 1
    multiindex = pd.MultiIndex.from_arrays(df.ffill(1).values[:2, 1:], names=['year', 'CANDIDATE'])
    return pd.DataFrame(df.values[2:, 1:], index=df.values[2:, 0], columns=multiindex)

def drop_redundant_rows(df):
    return df.drop([ np.nan,'Region', 'The Midwest', 'The Northeast', 'The South',
             'The West'])

def get_columns_with_counts(df, earliest_year = 1950):
    to_keep = [i for i, name in enumerate(df.columns.tolist())
                 if (type(name[0]) == int) and name[0] > earliest_year ]
    totals = [i for i, name in enumerate(df.columns.tolist())
                     if name[1] == 'Total']
    to_keep = [i for i in to_keep if i > totals[0] and i not in totals]

    return df.iloc[:, to_keep]

df = import_election_sheet()
df = drop_redundant_rows(df)
df = get_columns_with_counts(df)

# This is how we turn candidates and years into features
df = df.unstack().reset_index()

df['candidate'] = df.CANDIDATE.str.split('-').str[0].str.strip()
df['party'] = df.CANDIDATE.str.split('-').str[1].str.strip()

# Clean up data frames
df.drop('CANDIDATE', axis=1, inplace=True)
df.rename(columns={0: 'votes', 'level_2': 'state'}, inplace=True)

print(df.head())

if __name__ == '__main__':
    from us_state_abbrev import us_state_abbrev as state_abbrev
    state_abbrev['Washington DC']='DC'
    df['short_state'] = df.state.transform(lambda x: state_abbrev[x])
    df.to_csv('elections.csv', index=False)
