from config import *
from utils import *
from whoosh import index

# Max 12 different configuartions of Analyzer and Scoring
# Frequency must appear in at most 1 config
CONFIG = [['simple', 'frequency'],
          ['simple', 'tfidf'],
          ['standard', 'tfidf'],
          # fill this with the remaining pairings according to google sheet table
          # https://docs.google.com/spreadsheets/d/1xLCRqrfUH_aQZ9TyC4OL0s76VScsLx8rCiSLes9-hyM/edit#gid=0
          ]

DATASET = ['cranfield', 'time']


def run_config(index_dir, dataset, scoring_function):
    """ Return a dictionary of all metrics

    :param dataset: string
    :param scoring_function: Whoosh scoring object
    :return: dictionary
    """
    print(f"Index: {index_dir}")
    print(f"Dataset: {dataset}")
    print(f"Scoring function: {scoring_function.__class__.__name__}")

    # load selected dataset
    filtered_queries, queries_gt = load_dataset(dataset)

    # open index
    ix = index.open_dir(index_dir)

    # results for both sets of queries
    results_ids = get_results_ids(ix, scoring_function, filtered_queries)

    # compute metrics
    MRR = mean_reciprocal_rank(results_ids, queries_gt)

    # compute R-precision
    rp = r_precision(results_ids, queries_gt)
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
    print("\n" + "="*20 + "\n")


if __name__ == "__main__":
    for dataset in DATASET:
        for index_dir, scoring in CONFIG:
            # index pathname
            index_dir = INDEX_PATH + index_dir

            # run a single configuration test
            run_config(index_dir, dataset, SCORINGS[scoring])
            break
