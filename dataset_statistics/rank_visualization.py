import pandas as pd
import matplotlib.pyplot as plt 

def rank_visualization(df):
    df['bws_rank'] = df.rank(method='min', ascending=False)['bws_score']
    rank = df['bws_rank'].tolist()
    bws_list = df['bws_score'].tolist()
    min_rank = min(rank)
    max_bws = max(bws_list)
    max_rank = max(rank)
    min_bws = min(bws_list)
    p1 = [min_rank, max_rank]
    p2 = [max_bws, min_bws]
    plt.xlabel("Rank")
    plt.ylabel("BWS Score")
    plt.plot(p1, p2, linestyle = "dashed", color="red")
    plt.scatter(rank, bws_list, s=10)
    plt.show()


if __name__ == '__main__':
    postprocessed_df = pd.read_csv('/Users/kohtarotanaka/work/new_meme_dataset_2/new_meme_dataset_2/postprocess/postprocessed_dataset.csv')
    refined_df = pd.read_csv('/Users/kohtarotanaka/work/new_meme_dataset_2/new_meme_dataset_2/refinement/refined_dataset.csv')
    rank_visualization(refined_df)
