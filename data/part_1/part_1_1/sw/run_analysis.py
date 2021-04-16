from config import *
from utils import *
from whoosh import index
import matplotlib.pyplot as plt
LARGE_SIZE = 20
MEDIUM_SIZE = 15
SMALL_SIZE = 12

plt.rc('axes', labelsize=LARGE_SIZE)
plt.rc('xtick', labelsize=MEDIUM_SIZE)
plt.rc('ytick', labelsize=MEDIUM_SIZE)
plt.rc('legend', fontsize=SMALL_SIZE)

# Max 12 different configuartions of Analyzer and Scoring
# Frequency must appear in at most 1 config
CONFIG = [['stemming', 'bm25f', 0.8, 1.9],
          ['stemming', 'bm25f', 0.8, 1.5],
          ['stemming', 'bm25f', 0.7, 1.7],
          ['stemming', 'bm25f', 0.9, 1.5],
          ['stemming', 'bm25f', 0.8, 1.2],
          ['stemming', 'bm25f', 0.9],
          ['stemming', 'bm25f', 0.3, 1.2],
          ['stemming', 'bm25f', 0.4, 1.7],
          ['stemming', 'bm25f'],
          ['stemming', 'bm25f', 0.5, 1.5],
          ['stemming', 'bm25f', 0.2, 1.9],
          ['standard', 'bm25f']
          ]

DATASET = ['cranfield', 'time']


def parse_config(config_list):
    """

    :param config_list:
    :return:
    """
    n_params = len(config_list)
    config = dict()

    config['index'] = config_list[0]
    config['scoring_function'] = config_list[1]

    try:
        config['B'] = config_list[2]
    except IndexError:
        config['B'] = 0.75

    try:
        config['K1'] = config_list[3]
    except IndexError:
        config['K1'] = 1.2

    return config


def run_config(dataset, config, verbose=True):
    """ Return a dictionary of all metrics

    :param config: dictionary
    :param verbose: bool
    :param dataset: string
    :return: Metrics object
    """
    scoring_str = config['scoring_function']
    index_type = config['index']

    # index pathname
    index_dir = INDEX_PATH + index_type

    # selected scoring function
    scoring_function = SCORINGS[scoring_str]

    # scoring_function here is a Class name not an actual object
    if scoring_str == 'bm25f':
        B, K1 = config['B'], config['K1']
        scoring_function = scoring_function(B, K1)
        scoring_str = f"{scoring_str}({B},{K1})"

    # load selected dataset
    filtered_queries, queries_gt = load_dataset(dataset)

    # open index
    ix = index.open_dir(index_dir)

    # results for both sets of queries
    results_ids = get_results_ids(ix, scoring_function, filtered_queries)

    # string name of the preprocessing used
    index_type = index_dir.split('_')[-1]

    # save all performance metrics
    metrics = Metrics(index_type, dataset, scoring_str)
    metrics.compute_metrics(results_ids, queries_gt)

    if verbose:
        print(f"Index: {index_dir}")
        print(f"Dataset: {dataset}")
        print(f"Scoring function: {scoring_function.__class__.__name__}")
        metrics.print_metrics()

    return metrics


if __name__ == "__main__":
    metrics_list = {'cranfield': [], 'time': []}

    # iterate over both datasets and all available configurations
    for dataset in DATASET:
        for item in CONFIG:
            config = parse_config(item)

            # run a single configuration test
            metrics = run_config(dataset, config)
            metrics_list[dataset].append(metrics)

    # take top5 configurations according to MRR
    top5_cranfield = sorted(metrics_list['cranfield'], key=lambda x: x.MRR, reverse=True)[:5]
    top5_time = sorted(metrics_list['time'], key=lambda x: x.MRR, reverse=True)[:5]

    # make plots of NCDG@k and P@k
    datasets_df = list(map(dataframe_from_metrics, [top5_cranfield, top5_time]))
    stats = ["precision", "ncdg"]

    print("Saving plots...")
    for stat in stats:
        fig, axes = plt.subplots(1, 2, figsize=(15, 5))

        for i, dataset in enumerate(DATASET):
            plot_df(datasets_df[i], ax=axes[i], ylab=stat)
            axes[i].set_title(f"{stat}@k for {dataset} dataset", fontsize=MEDIUM_SIZE)

        fig.savefig(f"{stat}@k.png")
