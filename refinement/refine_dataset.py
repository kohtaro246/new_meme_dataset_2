import pandas as pd

def execute():
    df = pd.read_csv('/Users/kohtarotanaka/work/new_meme_dataset_2/new_meme_dataset_2/postprocess/postprocessed_dataset.csv')
    refinement_threshold = 0.5
    df = df[(df['bws_score'] >= refinement_threshold) | (df['bws_score'] <= -refinement_threshold)]
    print(df)

if __name__ == '__main__':
    execute()