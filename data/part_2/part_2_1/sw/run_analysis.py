from utils import *

TSV_FILENAME = ["data/BRUTE_FORCE_lyrics.tsv", "data/PRED_lyrics.tsv"]

if __name__ == "__main__":
    gt_path, pred_path = TSV_FILENAME

    # load near duplicates from tsv
    gt = load_near_duplicates_tsv(gt_path)
    pred = load_near_duplicates_tsv(pred_path)

    # performance analysis
    prob, false_pos, false_neg = near_duplicates_stats(gt, pred)

    print(f"Detection probability: {prob}")
    print(f"False positives: {false_pos}")
    print(f"False negatives: {false_neg}")
