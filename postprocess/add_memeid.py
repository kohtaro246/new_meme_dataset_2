import pandas as pd
from tqdm import tqdm

tqdm.pandas()

def add_memeid(input_df, result_df, tuples):
    with open(tuples) as f:
        bws_lines = f.readlines()

    memeids = []
    memeids_column = []
    for i, bws_line in enumerate(bws_lines):
        div = i // 3
        remainder = i % 3
        set_list = list(bws_line.replace("\n","").split("\t"))
        set_list = [int(i) for i in set_list]
        memeids += set_list
        if remainder == 2:
            assert len(memeids) == 12
            memeids_column.append(str(memeids))
            memeids = []
    assert len(input_df) == len(memeids_column)
    input_df['memeids'] = memeids_column
    
    def add_memeid_in_df(row):
        image_1 = row['Input.image_url_1']
        image_2 = row['Input.image_url_2']
        image_3 = row['Input.image_url_3']
        image_4 = row['Input.image_url_4']
        image_5 = row['Input.image_url_5']
        image_6 = row['Input.image_url_6']

        global input_df
        df_bool = (input_df['image_url_1'] == image_1) & (input_df['image_url_2'] == image_2) & (input_df['image_url_3'] == image_3) & (input_df['image_url_4'] == image_4) & (input_df['image_url_5'] == image_5) & (input_df['image_url_6'] == image_6)
        assert df_bool.sum() == 1
        memeids = input_df.loc[df_bool, 'memeids'].values
        if len(memeids) == 1:
            return memeids[0]

    result_df['memeids'] = result_df.progress_apply(add_memeid_in_df, axis=1)
    result_df.to_csv('raw_output/amt_result_with_memeid.csv', index=False)
            
if __name__ == '__main__':
    input_df = pd.read_csv('/Users/kohtarotanaka/work/new_meme_dataset_2/new_meme_dataset_2/amt_input_creation/amt_input_full.csv')
    result_df = pd.read_csv('/Users/kohtarotanaka/work/new_meme_dataset_2/new_meme_dataset_2/postprocess/raw_output/amt_result_full.csv')
    tuples = "/Users/kohtarotanaka/work/new_meme_dataset_2/new_meme_dataset_2/amt_input_creation/meme_items_24000.txt.tuples"
    add_memeid(input_df, result_df, tuples)

        