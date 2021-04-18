from whoosh import index
from config import *
from utils import *

if __name__ == "__main__":
    config = query_config()

    # index directory
    index_dir = config['path']
    scoring_function = config['scoring']

    print(f"Target directory: {index_dir}")
    print(f"Scoring function: {scoring_function.__class__.__name__}")

    # load selected dataset
    filtered_queries, queries_gt = load_dataset(config['dataset'])

    # open index
    ix = index.open_dir(index_dir)

    # results for both sets of queries
    results_ids = get_results_ids(ix, scoring_function, filtered_queries)

    # compute metrics
    MRR = mean_reciprocal_rank(results_ids, queries_gt)

    # compute R-precision
    rp = precision_at_k(results_ids, queries_gt)
    rps = compute_stats(rp)

    print()
    print(f"MRR: {MRR:.3f}\n")
    print("[R-Precision]")
    print(f"Mean: \t\t {rps['mean']}")
    print(f"Min: \t\t {rps['min']}")
    print(f"1st quartile:\t {rps['first_quartile']}")
    print(f"Median: \t {rps['median']}")
    print(f"3rd quartile:\t {rps['third_quartile']}")
    print(f"Max:\t\t {rps['max']}")

    # Precision at k plot
    rp_at_k = [compute_stats(precision_at_k(results_ids, queries_gt, k))['mean'] for k in K_VAL]
    print(f"P@k {rp_at_k}")

    # Normalized Discounted Cumulative Gain at k plot
    ndcg_at_k = [mean_ndcg(results_ids, queries_gt, k) for k in K_VAL]
    print(f"NDCG@k {ndcg_at_k}")
