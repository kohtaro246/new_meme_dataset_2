import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
import sys
from tqdm import tqdm
from statistics import mean, stdev
from scipy.stats import sem

sys.path.append('/Users/kohtarotanaka/work/new_meme_dataset_2/new_meme_dataset_2/postprocess')
from filter_hits import filter_hits

def get_relationships(result_df):
    relationships = []
    for _, row in tqdm(result_df.iterrows(), total=result_df.shape[0]):
        memeids = eval(row['memeids'])
        fourmemeids = []
        for i in range(1, 13):
            memeid = memeids[i-1]
            fourmemeids.append(memeid)
            if i % 4 == 0 and i // 4 == 1:
                idxs = [0,1,2,3]
                most_1 = row['Answer.choice-q26-1']
                least_1 = row['Answer.choice-q26-2']
                most_id = int(fourmemeids[int(most_1)-1])
                least_id = int(fourmemeids[int(least_1)-1])
                idx_list = [int(most_1)-1, int(least_1)-1]
                other_idxs = list(set(idxs) ^ set(idx_list))
                other_id_1 = int(fourmemeids[other_idxs[0]])
                other_id_2 = int(fourmemeids[other_idxs[1]])
                relationships += [[most_id, other_id_1], [most_id, other_id_2], [most_id, least_id], [other_id_1, least_id], [other_id_2, least_id]]
                fourmemeids = []

            elif i % 4 == 0 and i // 4 == 2:
                idxs = [0,1,2,3]
                most_1 = row['Answer.choice-q27-1']
                least_1 = row['Answer.choice-q27-2']
                most_id = int(fourmemeids[int(most_1)-1])
                least_id = int(fourmemeids[int(least_1)-1])
                idx_list = [int(most_1)-1, int(least_1)-1]
                other_idxs = list(set(idxs) ^ set(idx_list))
                other_id_1 = int(fourmemeids[other_idxs[0]])
                other_id_2 = int(fourmemeids[other_idxs[1]])
                relationships += [[most_id, other_id_1], [most_id, other_id_2], [most_id, least_id], [other_id_1, least_id], [other_id_2, least_id]]
                fourmemeids = []

            if i % 4 == 0 and i // 4 == 3:
                idxs = [0,1,2,3]
                most_1 = row['Answer.choice-q28-1']
                least_1 = row['Answer.choice-q28-2']
                most_id = int(fourmemeids[int(most_1)-1])
                least_id = int(fourmemeids[int(least_1)-1])
                idx_list = [int(most_1)-1, int(least_1)-1]
                other_idxs = list(set(idxs) ^ set(idx_list))
                other_id_1 = int(fourmemeids[other_idxs[0]])
                other_id_2 = int(fourmemeids[other_idxs[1]])
                relationships += [[most_id, other_id_1], [most_id, other_id_2], [most_id, least_id], [other_id_1, least_id], [other_id_2, least_id]]
                fourmemeids = []
    return relationships

def get_duplicate_list(relationships, dataset_df):
    bws_scores = []
    new_relationships = []
    for two_set in tqdm(relationships):
        memeid_1 = two_set[0]
        memeid_2 = two_set[1]
        bws_score_1 = dataset_df[dataset_df['memeid'] == memeid_1]['bws_score'].values
        bws_score_2 = dataset_df[dataset_df['memeid'] == memeid_2]['bws_score'].values
        if len(bws_score_1) == 0 or len(bws_score_2) == 0:
            continue
        else:
            bws_score_1 = bws_score_1[0]
            bws_score_2 = bws_score_2[0]
            bws_scores.append([bws_score_1, bws_score_2])
            new_relationships.append(two_set)
    relationships = new_relationships

    seen = []
    accuracies = []
    bws_diffs = []
    for i, two_set in enumerate(tqdm(relationships)):
        correct = 0
        incorrect = 0
        flip_two_set = [two_set[1], two_set[0]]
        if bws_scores[i][0] != bws_scores[i][1]:
            if (two_set not in seen) and (flip_two_set not in seen):
                if bws_scores[i][0] > bws_scores[i][1]:
                    correct += 1
                else:
                    incorrect += 1
                if two_set in relationships[i + 1:]:
                    if bws_scores[i][0] > bws_scores[i][1]:
                        correct = relationships[i + 1:].count(two_set)
                    else:
                        incorrect = relationships[i + 1:].count(two_set)

                if flip_two_set in relationships[i + 1:]:
                    if bws_scores[i][0] > bws_scores[i][1]:
                        incorrect = relationships[i + 1:].count(flip_two_set)
                    else:
                        correct = relationships[i + 1:].count(flip_two_set)
            if correct + incorrect > 0:
                accuracy = float(correct) / float(correct + incorrect)
                bws_diff = abs(bws_scores[i][0] - bws_scores[i][1])
                accuracies.append(accuracy)
                bws_diffs.append(bws_diff)
            seen.append(two_set)
        if i == len(relationships) - 2:
            break

    return seen, accuracies, bws_diffs

def calculate_statistics(accuracies, bws_diffs):
    minimum_score_diff = min(bws_diffs)
    maximum_score_diff = max(bws_diffs)
    score_range = maximum_score_diff - minimum_score_diff
    #print(range)
    mem = float(score_range) / 25   
    x = []
    y = []
    y2 = []
    num1 = minimum_score_diff + (mem/2)
    num2 = minimum_score_diff
    for i in range(24):
        indexes = [i for i, x in enumerate(bws_diffs) if x >= num2 and x < num2 + mem]
        if len(indexes) != 0: 
            per_instance_accuracies = []
            for index in indexes:
                per_instance_accuracies.append(accuracies[index])
            average = mean(per_instance_accuracies)
            standard_error = sem(per_instance_accuracies) 
            y.append(average)
            y2.append(standard_error)
            num1 += mem
            x.append(num1)
        else:
            pass
        num2 += mem
    return x, y, y2
    

    

def calculate_human_agreement(result_df, dataset_df):
    result_df = filter_hits(result_df, worktime_threshold=270)
    relationships = get_relationships(result_df)
    seen, accuracies, bws_diffs = get_duplicate_list(relationships, dataset_df)
    assert len(accuracies) == len(bws_diffs)
    x, y, y2 = calculate_statistics(accuracies, bws_diffs)
    plt.scatter(x, y, s=10, label='Average')
    plt.errorbar(x,y,yerr=y2, ecolor='black')
    plt.xlabel('Score Difference')
    plt.ylabel("Human Agreement")
    plt.show()





if __name__ == '__main__':
    result_df = pd.read_csv('/Users/kohtarotanaka/work/new_meme_dataset_2/new_meme_dataset_2/postprocess/raw_output/amt_result_with_memeid.csv')
    dataset_df = pd.read_csv('/Users/kohtarotanaka/work/new_meme_dataset_2/new_meme_dataset_2/postprocess/postprocessed_dataset.csv')
    calculate_human_agreement(result_df, dataset_df)