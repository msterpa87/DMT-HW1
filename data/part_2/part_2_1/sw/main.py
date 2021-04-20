from utils import *


if __name__ == "__main__":
    args = analysis_config()
    gt_path, pred_path = args.ground_truth, args.pred

    # load near duplicates from tsv
    gt = load_near_duplicates_tsv(gt_path)
    pred = load_near_duplicates_tsv(pred_path)

    # performance analysis
    prob, false_pos, false_neg = near_duplicates_stats(gt, pred)

    print(f"Found {len(pred)} near duplicates")
    print(f"Detection probability: {prob:.3f}")
    print(f"False positives: {false_pos}")
    print(f"False negatives: {false_neg}")
