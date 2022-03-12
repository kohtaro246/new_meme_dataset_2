import pandas as pd

def filter_hits(df, worktime_threshold):
    '''
    1. select approved
    2. select hits taken more than 90 sec to complete
    3. if annotator selects the same meme for best and worst, remove the hit
    4. if annotator inputs less than 3 alphabet as humor anchor except for dummy, remove the hit
    5. if annotator inputs nie for all humor anchors
    '''

    def not_all_short_alphabet(row):
        for i in range(12):
            question_num = (i + 1) * 2
            if len(row[f'Answer.q{question_num}-word1']) >= 3:
                return True
        return False

    def not_all_nie(row):
        for i in range(12):
            question_num = (i + 1) * 2
            if row[f'Answer.q{question_num}-word1'].lower() != "nie":
                return True
        return False

    # select approved
    df = df[df['AssignmentStatus'] == "Approved"]
    # select hits taken more than 90 sec to complete
    df = df[df['WorkTimeInSeconds'] > worktime_threshold]
    # if annotator selects the same meme for best and worst, remove the hit
    df_bool = ~((df['Answer.choice-q26-1'] == df['Answer.choice-q26-2']) | (df['Answer.choice-q27-1'] == df['Answer.choice-q27-2']) | (df['Answer.choice-q28-1'] == df['Answer.choice-q28-2']))
    df = df[df_bool]
    # if annotator inputs only 1 word as humor anchor except for dummy, remove the hit
    df['not_all_short_alphabet'] = df.apply(not_all_short_alphabet, axis=1)
    df = df[df['not_all_short_alphabet']]
    df = df.drop(columns='not_all_short_alphabet')
    # if annotator inputs nie for all humor anchors
    df['not_all_nie'] = df.apply(not_all_nie, axis=1)
    df = df[df['not_all_nie']]
    df = df.drop(columns='not_all_nie')
    return df

if __name__ == '__main__':
    df = pd.read_csv('/Users/kohtarotanaka/work/new_meme_dataset_2/new_meme_dataset_2/postprocess/raw_output/amt_result_full.csv')
    df = filter_hits(df, 120)
    df.to_csv('check.csv', index=False)