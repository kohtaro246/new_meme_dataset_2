import pandas as pd

def humor_binary_class(bws_score):
    if bws_score > 0:
        return 1
    else:
        return 0

def execute():
    df = pd.read_csv('/Users/kohtarotanaka/work/new_meme_dataset_2/new_meme_dataset_2/postprocess/postprocessed_dataset.csv')
    refinement_threshold = 0.4
    df = df[(df['bws_score'] >= refinement_threshold) | (df['bws_score'] <= -refinement_threshold)]
    df['humor_binary_class'] = df['bws_score'].apply(humor_binary_class)
    df.to_csv('refined_dataset_4.csv', index=False)

if __name__ == '__main__':
    execute()