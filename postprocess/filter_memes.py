import pandas as pd

def filter_memes(df, eval_count_threshold, not_english_threshold):
    # too few evalation counts
    df = df[df['evaluated_count'] >= eval_count_threshold]
    # not in English
    df = df.dropna(subset=['uppercaption', 'lowercaption'])
    # have only upper or lower caption
    df = df[df['nie_count'] < not_english_threshold]
    return df

if __name__ == '__main__':
    df = pd.read_csv("check.csv")
    df = filter_memes(df, 3, 3)
    df.to_csv('check_2.csv', index=False)

