'''
1. identicalなrowを除く
encodingでフィルタをかけて、strに変換して、captionを小文字で統一
2. テキストをフィルタする
4. caption数を80以上あるものに限定する？

'''

import pandas as pd 

from encoding_wordcount_filter import encoding_wordcount_filter
from word_profanity_filter import word_profanity_filter


def execute():
    def _convert_to_str(s):
        return str(s)

    def del_less_than_n(df, n):
        filename_list = df['filename'].unique().tolist()
        for filename in filename_list:
            meme_count = (df['filename'] == filename).sum()
            if meme_count < n:
                df = df[df['filename'] != filename]
        return df

    image_directory = '/home/mil/k-tanaka/new_meme_dataset_2/new_meme_dataset_2/scraping/memes/'
    df = pd.read_csv('/home/mil/k-tanaka/new_meme_dataset_2/new_meme_dataset_2/scraping/csv_files/edited_scraped_memes.csv')

    df = df.drop_duplicates()

    df['uppercaption'] = df['uppercaption'].map(_convert_to_str)
    df['lowercaption'] = df['lowercaption'].map(_convert_to_str)

    print("filter by encoding and wordcount")
    df = encoding_wordcount_filter(df)
    df = df[df['encoding_wordcount']]

    print("filter by word_profanity")
    df = word_profanity_filter(df)
    df = df[df['word_profanity']]

    df = del_less_than_n(df, 80)
    print(len(df))
    print(len(df['filename'].unique().tolist()))

    

    
    #df.to_csv('del_dataset.csv', index=False)

if __name__ == '__main__':
    execute()



