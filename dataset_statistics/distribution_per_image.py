import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from statistics import mean, stdev
from scipy.stats import sem


def create_bws_distribution_per_image(df):
    grouped_df = df.groupby('filename')
    statistics_df = grouped_df["bws_score"].agg([np.mean, sem, 'count']).sort_values('mean')
    statistics_df.to_csv('check_statistics.csv', index=False)
    



if __name__ == '__main__':
    postprocessed_df = pd.read_csv('/Users/kohtarotanaka/work/new_meme_dataset_2/new_meme_dataset_2/postprocess/postprocessed_dataset.csv')
    refined_df = pd.read_csv('/Users/kohtarotanaka/work/new_meme_dataset_2/new_meme_dataset_2/refinement/refined_dataset.csv')
    create_bws_distribution_per_image(postprocessed_df)
