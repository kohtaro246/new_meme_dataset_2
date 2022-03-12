import pandas as pd

from filter_hits import filter_hits
from add_annotations import add_annotations
from filter_memes import filter_memes


def execute():
    result_df = pd.read_csv('/Users/kohtarotanaka/work/new_meme_dataset_2/new_meme_dataset_2/postprocess/raw_output/amt_result_with_memeid.csv')
    dataset_df = pd.read_csv('/Users/kohtarotanaka/work/new_meme_dataset_2/new_meme_dataset_2/preprocess/preprocessed_dataset.csv')

    # filter poor quality hits based on approval, worktime, bws selection, and humor anchor
    print("-- filtering poor quality hits --")
    result_df = filter_hits(result_df, worktime_threshold=270)
    # add annotations to dataset csv
    print("-- adding annotations to dataset --")
    dataset_df = add_annotations(result_df, dataset_df)
    # filter memes that have too few evalation counts, that are not in English, or that have only upper or lower caption
    print("-- filtering memes not meeting requirements --")
    dataset_df = filter_memes(dataset_df, eval_count_threshold=3, not_english_threshold=3)

    dataset_df.to_csv('postprocessed_dataset.csv', index=False)


if __name__ == '__main__':
    execute()
