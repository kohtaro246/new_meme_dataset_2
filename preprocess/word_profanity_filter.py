import profanity_filter.profanity_filter as profanity_filter
import pandas as pd
from tqdm import tqdm
tqdm.pandas()
proffilter = profanity_filter.ProfanityFilter()

def word_profanity_filter(df):
    def _create_profanity_flag(row):
        global proffilter
        uppercaption = str(row['uppercaption'])
        lowercaption = str(row['lowercaption'])
        if proffilter.isProfane(uppercaption) or proffilter.isProfane(lowercaption):
            return False
        else:
            return True
    
    df['word_profanity'] = df.progress_apply(_create_profanity_flag, axis=1)
    return df


if __name__ == '__main__':
    df = pd.read_csv('/home/mil/k-tanaka/new_meme_dataset/scraping/scraped_memes.csv')
    df = word_profanity_filter(df)
    df[df['word_profanity'] == False].to_csv('check.csv', index=False)