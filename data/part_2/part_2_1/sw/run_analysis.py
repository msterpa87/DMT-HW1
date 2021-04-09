from utils import *

DUPLICATE_GT = "BRUTE_FORCE_near_duplicates.tsv"
DUPLICATE_PRED = "PRED_near_duplicates.tsv"

if __name__ == "__main__":
    # load near duplicates from tsv
    gt = load_near_duplicates_tsv(DUPLICATE_GT)
    pred = load_near_duplicates_tsv(DUPLICATE_PRED)

    # performance analysis
    prob, false_pos, false_neg = near_duplicates_stats(gt, pred)

    print(f"Detection probability: {prob}")
    print(f"False positives: {false_pos}")
    print(f"False negatives: {false_neg}")
