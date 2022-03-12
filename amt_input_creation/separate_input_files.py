import pandas as pd

df = pd.read_csv('amt_input_full.csv')
sep_df = df[9000:]
sep_df.to_csv('amt_input_4.csv', index=False)