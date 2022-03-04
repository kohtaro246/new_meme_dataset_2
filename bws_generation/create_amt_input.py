import pandas as pd



def create_amt_input(data_df, tuples):
    input_columns = ['image_url_1','caption_1_1','caption_1_2','image_url_2','caption_2_1','caption_2_2','image_url_3','caption_3_1','caption_3_2','image_url_4','caption_4_1','caption_4_2','image_url_5','caption_5_1','caption_5_2','image_url_6','caption_6_1','caption_6_2','image_url_7','caption_7_1','caption_7_2','image_url_8','caption_8_1','caption_8_2','image_url_9','caption_9_1','caption_9_2','image_url_10','caption_10_1','caption_10_2','image_url_11','caption_11_1','caption_11_2','image_url_12','caption_12_1','caption_12_2','image_url_13','caption_13_1','caption_13_2']
    input_df = pd.DataFrame(columns=input_columns)

    with open(tuples) as f:
        bws_lines = f.readlines()

    row_list = []
    uppercaptions = []
    lowercaptions = []
    counter = 0
    for i, bws_line in enumerate(bws_lines):
        set_list = list(bws_line.replace("\n","").split("\t"))
        set_list = [int(i) for i in set_list]

        
        for memeid in set_list:
            memeid = int(memeid)
            uppercaptions.append(data_df.loc[data_df['memeid'] == memeid, 'uppercaption'].values[0])
            lowercaptions.append(data_df.loc[data_df['memeid'] == memeid, 'lowercaption'].values[0])
        print(uppercaptions)

if __name__ == '__main__':
    data_df = pd.read_csv('/home/mil/k-tanaka/new_meme_dataset_2/new_meme_dataset_2/preprocess/preprocessed_dataset.csv')
    tuples = "meme_items_24000.txt.tuples"
    create_amt_input(data_df, tuples)

    