import pandas as pd 
from tqdm import tqdm
tqdm.pandas()

def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

def meets_wordcount_requirement(uppercaption, lowercaption):
    caption = uppercaption + ' ' + lowercaption
    uppercaption_count = uppercaption.split()
    lowercaption_count = lowercaption.split()
    caption_count = caption.split()
    if len(uppercaption_count) != 0 and len(lowercaption_count) != 0 and len(caption_count) < 26:
        return True
    else:
        return False

def encoding_wordcount_filter(df):
    def _create_encoding_wordcount_flag(row):
        uppercaption = str(row['uppercaption'])
        lowercaption = str(row['lowercaption'])
        #if isEnglish(uppercaption) and isEnglish(lowercaption) and meets_wordcount_requirement(uppercaption, lowercaption):
        if isEnglish(uppercaption) and isEnglish(lowercaption):
            return True
        else:
            return False

    df['encoding_wordcount'] = df.progress_apply(_create_encoding_wordcount_flag, axis=1)
    return df

if __name__ == '__main__':
    df = pd.read_csv('/home/mil/k-tanaka/new_meme_dataset/scraping/scraped_memes.csv')
    df = encoding_wordcount_filter(df)
    df[df['encoding_wordcount'] == False].to_csv('check.csv', index=False)