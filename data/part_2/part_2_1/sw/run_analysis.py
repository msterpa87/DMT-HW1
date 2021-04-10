from utils import *

TSV_FILES = {"lyrics": ["data/BRUTE_FORCE_lyrics.tsv", "data/PRED_lyrics.tsv"],
             "title": ["data/BRUTE_FORCE_title.tsv", "data/PRED_title.tsv"]}

if __name__ == "__main__":
    args = analysis_config()
    gt_path, pred_path = TSV_FILES[args.field]

    # load near duplicates from tsv
    gt = load_near_duplicates_tsv(gt_path)
    pred = load_near_duplicates_tsv(pred_path)

    # performance analysis
    prob, false_pos, false_neg = near_duplicates_stats(gt, pred)

    print(f"Detection probability: {prob}")
    print(f"False positives: {false_pos}")
    print(f"False negatives: {false_neg}")
