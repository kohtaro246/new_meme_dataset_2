import pandas as pd

def del_less_than_n(df, n, upper_n):
        filename_list = df['filename'].unique().tolist()
        for filename in filename_list:
            meme_count = (df['filename'] == filename).sum()
            if meme_count > upper_n:
                filtered_df = df[df['filename'] == filename]
                filtered_df = filtered_df.sort_values(by=['upvote'], ascending=False)
                del_index = list(filtered_df[upper_n:].index)
                df = df.drop(del_index)

            if meme_count < n:
                df = df[df['filename'] != filename]
        return df

if __name__ == '__main__':
    df = pd.read_csv('/home/mil/k-tanaka/new_meme_dataset_2/new_meme_dataset_2/scraping/csv_files/edited_scraped_memes_new.csv')
    df = del_less_than_n(df, 30, 80)
    print(len(df))
    df.to_csv('check.csv', index=False)
    