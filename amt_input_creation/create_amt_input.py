import pandas as pd
from tqdm import tqdm



def create_amt_input(data_df, tuples, url_df):
    input_columns = ['image_url_1','caption_1_1','caption_1_2','image_url_2','caption_2_1','caption_2_2','image_url_3','caption_3_1','caption_3_2','image_url_4','caption_4_1','caption_4_2','image_url_5','caption_5_1','caption_5_2','image_url_6','caption_6_1','caption_6_2','image_url_7','caption_7_1','caption_7_2','image_url_8','caption_8_1','caption_8_2','image_url_9','caption_9_1','caption_9_2','image_url_10','caption_10_1','caption_10_2','image_url_11','caption_11_1','caption_11_2','image_url_12','caption_12_1','caption_12_2','image_url_13','caption_13_1','caption_13_2']
    input_df = pd.DataFrame(columns=input_columns)

    with open(tuples) as f:
        bws_lines = f.readlines()

    row_list = []

    dummy_uppercaption1 = "légende supérieure"
    dummy_lowercaption1 = "légende inférieure"
    dummy_url1 = "http://drive.google.com/uc?export=view&id=1zrGw8fsRI0_kIoSKGY5y5JiZ8h3UFRqa"
    dummy_uppercaption2 = "obere Beschriftung"
    dummy_lowercaption2 = "untere Bildunterschrift"
    dummy_url2 = "http://drive.google.com/uc?export=view&id=1ipUPyzJqtTWjo0md3IC5c3q3XUPkL_Qb"
    dummy_uppercaption3 = "övre bildtext"
    dummy_lowercaption3 = "lägre bildtext"
    dummy_url3 = "http://drive.google.com/uc?export=view&id=1H-9NB0_rgsTICmod9mIY8wDoHugLkShN"
    counter = 0
    for i, bws_line in enumerate(tqdm(bws_lines)):
        set_list = list(bws_line.replace("\n","").split("\t"))
        set_list = [int(i) for i in set_list]

        
        for memeid in set_list:
            memeid = int(memeid)
            uppercaption = data_df.loc[data_df['memeid'] == memeid, 'uppercaption'].values[0]
            lowercaption = data_df.loc[data_df['memeid'] == memeid, 'lowercaption'].values[0]
            filename = data_df.loc[data_df['memeid'] == memeid, 'filename'].values[0]
            template_url = url_df.loc[url_df['filename'] == filename, 'url'].values[0]
            row_list.append(template_url)
            row_list.append(uppercaption)
            row_list.append(lowercaption)
        
        if i % 3 == 2:
            if counter % 3 == 0:
                row_list.append(dummy_url1)
                row_list.append(dummy_uppercaption1)
                row_list.append(dummy_lowercaption1)
            elif counter % 3 == 1:
                row_list.append(dummy_url2)
                row_list.append(dummy_uppercaption2)
                row_list.append(dummy_lowercaption2)
            else:
                row_list.append(dummy_url3)
                row_list.append(dummy_uppercaption3)
                row_list.append(dummy_lowercaption3)
                
            assert len(row_list) == len(input_columns)
            row_list_series = pd.Series(row_list, index=input_columns)
            input_df = input_df.append(row_list_series, ignore_index=True)
            row_list = []
            counter += 1
        #print(input_df)
    return input_df


        


if __name__ == '__main__':
    data_df = pd.read_csv('/Users/kohtarotanaka/work/new_meme_dataset_2/new_meme_dataset_2/preprocess/preprocessed_dataset.csv')
    url_df = pd.read_csv('meme_url.csv')
    tuples = "meme_items_24000.txt.tuples"
    input_df = create_amt_input(data_df, tuples, url_df)
    print(input_df)
    input_df.to_csv('amt_input_full.csv', index=False)

    