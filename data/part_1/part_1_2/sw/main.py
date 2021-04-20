from utils import *

if __name__ == "__main__":
    datasets = [f"../dataset/part_1_2__Results_SE_{i}.tsv" for i in [1, 2, 3]]

    # loading ground truth and search engine results
    gt = load_ground_truth("../dataset/part_1_2__Ground_Truth.tsv")
    pred = [queries_with_gt(load_queries_results(d), gt) for d in datasets]

    # computing precision at k=4 stats
    precision_at_4 = [precision_at_k(pred[i], gt, 4) for i in range(3)]
    precision_stats = [compute_stats(x) for x in precision_at_4]
    print_stats(precision_stats, title="Precision at 4")

    # computing recall at k=4 stats
    recall_at_4 = [recall_at_k(pred[i], gt, 4) for i in range(3)]
    recall_stats = [compute_stats(x) for x in recall_at_4]
    print_stats(recall_stats, title="Recall at 4")

    # Average F-score
    fscore = [fscore_from_pr(p, r) for p, r in zip(precision_at_4, recall_at_4)]
    print_fscores(fscore)
