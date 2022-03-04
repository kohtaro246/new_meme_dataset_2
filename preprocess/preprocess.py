'''
1. identicalなrowを除く
encodingでフィルタをかけて、strに変換して、captionを小文字で統一
2. テキストをフィルタする
4. caption数を80以上あるものは80に統一し、それ以外はそのまま入れる

'''

import pandas as pd 

from encoding_wordcount_filter import encoding_wordcount_filter
from word_profanity_filter import word_profanity_filter
from caption_count import del_less_than_n
from sort_data import sort_df


def execute():
    def _convert_to_str(s):
        return str(s)


    image_directory = '/home/mil/k-tanaka/new_meme_dataset_2/new_meme_dataset_2/scraping/memes/'
    df = pd.read_csv('/home/mil/k-tanaka/new_meme_dataset_2/new_meme_dataset_2/scraping/csv_files/edited_scraped_memes_new.csv')
    print(f"orig len: {len(df)}")

    df = df.drop_duplicates()
    print(f"after drop len: {len(df)}")

    #df['uppercaption'] = df['uppercaption'].map(_convert_to_str)
    #df['lowercaption'] = df['lowercaption'].map(_convert_to_str)

    print("filter by encoding and wordcount")
    df = encoding_wordcount_filter(df)
    df = df[df['encoding_wordcount']]
    print(f"after filter by encoding and wordcount: {len(df)}")

    print("filter by word_profanity")
    df = word_profanity_filter(df)
    df = df[df['word_profanity']]
    print(f"after profanity filter: {len(df)}")

    df = del_less_than_n(df, 11, 75)
    

    df = sort_df(df)
    print(f"final meme num: {len(df)}")
    print(f"final template image num {len(df['filename'].unique().tolist())}")

    seq = [i for i in range(1, 24001)]
    df['memeid'] = seq
    df = df.reindex(columns=['memeid', 'url', 'filename', 'uppercaption', 'lowercaption', 'views', 'upvote'])
    print(df)
    df.to_csv('preprocessed_dataset.csv', index=False)

if __name__ == '__main__':
    execute()



