import pandas as pd


df1 = pd.read_csv('csv_files/scraped_memes_10.csv')
df2 = pd.read_csv('csv_files/scraped_memes_11_20.csv')
df3 = pd.read_csv('csv_files/scraped_memes_21_30.csv')
df4 = pd.read_csv('csv_files/scraped_memes_21_30_2.csv')
df5 = pd.read_csv('csv_files/scraped_memes_31_40.csv')

df = df1
df = pd.concat([df, df2], ignore_index=True)
df = pd.concat([df, df3], ignore_index=True)
df = pd.concat([df, df4], ignore_index=True)
df = pd.concat([df, df5], ignore_index=True)

df.to_csv('csv_files/scraped_memes.csv', index=False)