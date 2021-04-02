from whoosh import index, scoring
from config import *
from utils import *

if __name__ == "__main__":
    config = query_config()

    # index directory
    index_dir = config['path']
    scoring_frequency = config['scoring']

    print(f"Target directory: {index_dir}")
    print(f"Scoring function: {scoring_frequency.__class__.__name__}")

    # loading queries
    cranfield_queries = load_queries(CRANFIELD_QUERY)
    time_queries = load_queries(TIME_QUERY)

    # loading ground truth
    cranfield_gt = load_ground_truth(CRANFIELD_GT)
    time_gt = load_ground_truth(TIME_GT)

    # test only on queries for which both str and gt are available
    filtered_cranfield = queries_with_gt(cranfield_queries, cranfield_gt)

    # open index
    ix = index.open_dir(index_dir)

    MRR = mean_reciprocal_rank(ix, scoring_frequency, filtered_cranfield, cranfield_gt)

    print(f"MRR = {MRR}")
