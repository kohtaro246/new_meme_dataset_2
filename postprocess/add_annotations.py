from unittest import result
import pandas as pd
import numpy as np
from tqdm import tqdm

def count_best_worst(row, best_count, worst_count, item_count):
    memeids = eval(row['memeids'])
    fourmemeids = []

    for i in range(1, 13):
        memeid = memeids[i-1]
        item_count[int(memeid)-1] += 1
        fourmemeids.append(memeid)
        if i % 4 == 0 and i // 4 == 1:
            most_1 = row['Answer.choice-q26-1']
            least_1 = row['Answer.choice-q26-2']
            most_id = int(fourmemeids[int(most_1)-1]) - 1
            least_id = int(fourmemeids[int(least_1)-1]) - 1
            best_count[most_id] += 1
            worst_count[least_id] += 1
            fourmemeids = []
        if i % 4 == 0 and i // 4 == 2:
            most_1 = row['Answer.choice-q27-1']
            least_1 = row['Answer.choice-q27-2']
            most_id = int(fourmemeids[int(most_1)-1]) - 1
            least_id = int(fourmemeids[int(least_1)-1]) - 1
            best_count[most_id] += 1
            worst_count[least_id] += 1
            fourmemeids = []
        if i % 4 == 0 and i // 4 == 3:
            most_1 = row['Answer.choice-q28-1']
            least_1 = row['Answer.choice-q28-2']
            most_id = int(fourmemeids[int(most_1)-1]) - 1
            least_id = int(fourmemeids[int(least_1)-1]) - 1
            best_count[most_id] += 1
            worst_count[least_id] += 1
            fourmemeids = []
    return best_count, worst_count, item_count

def calculate_bws(best_count, worst_count, item_count):
    np.seterr(invalid='ignore')
    nominator = best_count - worst_count
    return nominator / item_count


def count_moral_flag(row, moral_count):
    memeids = eval(row['memeids'])
    for i, memeid in enumerate(memeids):
        question_num = 2 * i + 1
        if int(row[f'Answer.choice-q{question_num}']) == 2:
            moral_count[memeid - 1] += 1
    return moral_count

def add_humor_anchor(row, dataset_df, humor_anchor_list):
    memeids = eval(row['memeids'])
    for i, memeid in enumerate(memeids):
        question_num = (i + 1) * 2
        word_dict = humor_anchor_list[memeid - 1]
        for j in range(1, 4):
            humor_anchor = str(row[f'Answer.q{question_num}-word{j}']).lower()
            if not (pd.isna(dataset_df.loc[dataset_df['memeid'] == memeid, "uppercaption"].values[0]) or pd.isna(dataset_df.loc[dataset_df['memeid'] == memeid, "lowercaption"].values[0])):
                if humor_anchor in dataset_df.loc[dataset_df['memeid'] == memeid, "uppercaption"].values[0].split(' ') or humor_anchor in dataset_df.loc[dataset_df['memeid'] == memeid, "lowercaption"].values[0].split(' '):
                    if humor_anchor in word_dict:
                        word_dict[humor_anchor] += 1
                    else:
                        word_dict[humor_anchor] = 1
        humor_anchor_list[memeid - 1] = word_dict
    return humor_anchor_list

def count_nie(row, nie_count):
    memeids = eval(row['memeids'])
    for i, memeid in enumerate(memeids):
        question_num = (i + 1) * 2
        humor_anchor = str(row[f'Answer.q{question_num}-word1']).lower()
        if humor_anchor == 'nie':
            nie_count[memeid - 1] += 1
    return nie_count


def add_annotations(result_df, dataset_df):
    best_count = np.zeros(24000, dtype=int)
    worst_count = np.zeros(24000, dtype=int)
    item_count = np.zeros(24000, dtype=int)
    bws_score = np.zeros(24000, dtype=float)
    moral_count = np.zeros(24000, dtype=int)
    humor_anchor_list = [{} for _ in range(24000)]
    nie_count = np.zeros(24000, dtype=int)

    for _, row in tqdm(result_df.iterrows(), total=result_df.shape[0]):
        best_count, worst_count, item_count = count_best_worst(row, best_count, worst_count, item_count)
        moral_count = count_moral_flag(row, moral_count)
        humor_anchor_list = add_humor_anchor(row, dataset_df, humor_anchor_list)
        nie_count = count_nie(row, nie_count)

    bws_score = calculate_bws(best_count, worst_count, item_count)
    dataset_df['bws_score'] = bws_score
    dataset_df['evaluated_count'] = item_count
    dataset_df['best_count'] = best_count
    dataset_df['worst_count'] = worst_count
    dataset_df['moral_count'] = moral_count
    dataset_df['humor_anchor'] = humor_anchor_list
    dataset_df['nie_count'] = nie_count
    dataset_df = dataset_df[dataset_df['evaluated_count'] != 0]
    dataset_df = dataset_df.sort_values(by=['bws_score'], ascending=False)
    return dataset_df
    

if __name__ == '__main__':
    result_df = pd.read_csv('/Users/kohtarotanaka/work/new_meme_dataset_2/new_meme_dataset_2/postprocess/raw_output/amt_result_with_memeid.csv')
    dataset_df = pd.read_csv('/Users/kohtarotanaka/work/new_meme_dataset_2/new_meme_dataset_2/preprocess/preprocessed_dataset.csv')
    dataset_df = add_annotations(result_df, dataset_df)
    dataset_df.to_csv('check.csv', index=False)