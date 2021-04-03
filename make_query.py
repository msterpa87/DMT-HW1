from whoosh import index, scoring
from config import *
from utils import *

if __name__ == "__main__":
    config = query_config()

    # index directory
    index_dir = config['path']
    scoring_function = config['scoring']

    print(f"Target directory: {index_dir}")
    print(f"Scoring function: {scoring_function.__class__.__name__}")

    # loading queries
    cranfield_queries = load_queries(CRANFIELD_QUERY)
    time_queries = load_queries(TIME_QUERY)

    # loading ground truth
    cranfield_gt = load_ground_truth(CRANFIELD_GT)
    time_gt = load_ground_truth(TIME_GT)

    # test only on queries for which both str and gt are available
    filtered_cranfield = queries_with_gt(cranfield_queries, cranfield_gt)
    filtered_time = queries_with_gt(time_queries, time_gt)

    # open index
    ix = index.open_dir(index_dir)

    # get doc ids for each query
    results_ids = get_results_ids(ix, scoring_function, filtered_cranfield)

    # compute metrics
    MRR = mean_reciprocal_rank(results_ids, cranfield_gt)

    # compute R-precision
    rp = r_precision(results_ids, cranfield_gt)
    rps = r_precision_stats(rp)

    print()
    print(f"MRR: {MRR}\n")
    print("[R-Precision]")
    print(f"Mean: \t\t {rps['mean']}")
    print(f"Min: \t\t {rps['min']}")
    print(f"1st quartile:\t {rps['first_quartile']}")
    print(f"Median: \t {rps['median']}")
    print(f"3rd quartile:\t {rps['third_quartile']}")
    print(f"Max:\t\t {rps['max']}")