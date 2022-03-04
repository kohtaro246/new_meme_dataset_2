import pandas as pd 

def sort_df(df):
    file_group_sum = df.groupby(['filename']).sum()
    file_group_sum = file_group_sum.sort_values(by=['upvote'], ascending=False)
    file_group_sum_series = file_group_sum['upvote']
    file_count = df['filename'].value_counts(sort=True)
    file_df = pd.concat([file_count, file_group_sum_series], axis=1)
    file_df = file_df.sort_values(by=['filename', 'upvote'], ascending=False)
    file_df = file_df[:500]
    filenames = file_df.index.values
    df = df[df['filename'].isin(file_df.index.values)]
    counter = 0
    for filename in filenames:
        if counter == 140:
            break
        filtered_df = df[df['filename'] == filename]
        del_index = filtered_df[-1:].index.values
        df = df.drop(del_index)
        counter += 1
    df = df.drop(['encoding_wordcount', 'word_profanity'], axis=1)
    return df


    


if __name__ == '__main__':
    df = pd.read_csv('preprocessed_dataset_2.csv')
    df = sort_df(df)
    print(df)