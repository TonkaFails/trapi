import pandas as pd

df = pd.read_csv('data/account_transactions.csv', sep=';')

# calculate share delta
df = df[df['Type'].isin(['Buy', 'Sell'])].copy()
df['Shares'] = pd.to_numeric(df['Shares'], errors='coerce')
df.loc[df['Type'] == 'Sell', 'Shares'] *= -1

depot = df.groupby(['ISIN', 'Note'])['Shares'].sum().reset_index()
depot = depot[depot['Shares'] > 0]

depot.to_csv('data/current_depot.csv', index=False)