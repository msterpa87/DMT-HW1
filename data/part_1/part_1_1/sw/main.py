from config import *
from utils import *
from whoosh import index
import matplotlib.pyplot as plt
import pickle
LARGE_SIZE = 20
MEDIUM_SIZE = 15
SMALL_SIZE = 12

# setup fontsize in plots
plt.rc('axes', labelsize=LARGE_SIZE)
plt.rc('xtick', labelsize=MEDIUM_SIZE)
plt.rc('ytick', labelsize=MEDIUM_SIZE)
plt.rc('legend', fontsize=SMALL_SIZE)

# best 12 different configurations of Analyzer and Scoring
CONFIG = [['stemming', 'bm25f', 0.7, 1.7],
          ['stemming', 'bm25f', 0.8, 1.5],
          ['stemming', 'bm25f', 0.8, 1.9],
          ['stemming', 'bm25f', 0.9, 1.5],
          ['stemming', 'bm25f'],
          ['stemming', 'bm25f', 0.4, 1.7],
          ['stemming', 'bm25f', 0.8, 1.2],
          ['stemming', 'bm25f', 0.9],
          ['stemming', 'bm25f', 0.5, 1.5],
          ['stemming', 'bm25f', 0.3, 2],
          ['stemming', 'bm25f', 0.2, 1.9],
          ['standard', 'bm25f', 0.4, 1.7],
          ]

DATASET = ['cranfield', 'time']


def parse_config(config_list):
    """ Takes a configuration from CONFIG and returns a dictionary
        with all the selected parameters

    :param config_list: list of strings/floats
        a list from CONFIG with 2 strings + 2 optional floats
    :return: dictionary
    """
    config_dict = dict()

    config_dict['index'] = config_list[0]
    config_dict['scoring_function'] = config_list[1]

    try:
        config_dict['B'] = config_list[2]
    except IndexError:
        config_dict['B'] = 0.75

    try:
        config_dict['K1'] = config_list[3]
    except IndexError:
        config_dict['K1'] = 1.2

    return config_dict


def run_config(dataset_name, config_dict, verbose=True):
    """ Return a dictionary of all metrics

    :param config_dict: dictionary
    :param verbose: bool
    :param dataset_name: string
    :return: Metrics object
    """
    scoring_str = config_dict['scoring_function']
    index_type = config_dict['index']

    # index pathname
    index_dir = f"{INDEX_PATH}_{dataset_name}_{index_type}"

    # selected scoring function
    scoring_function = SCORINGS[scoring_str]

    # scoring_function here is a Class name not an actual object
    if scoring_str == 'bm25f':
        B, K1 = config_dict['B'], config_dict['K1']
        scoring_function = scoring_function(B, K1)
        scoring_str = f"{scoring_str}({B},{K1})"

    # load selected dataset
    filtered_queries, queries_gt = load_dataset(dataset_name)

    # open index
    ix = index.open_dir(index_dir)

    # results for both sets of queries
    results_ids = get_results_ids(ix, scoring_function, filtered_queries)

    # string name of the preprocessing used
    index_type = index_dir.split('_')[-1]

    # save all performance metrics
    m = Metrics(index_type, dataset_name, scoring_str)
    m.compute_metrics(results_ids, queries_gt)

    if verbose:
        print(f"Index: {index_dir}")
        print(f"Dataset: {dataset_name}")
        print(f"Scoring function: {scoring_function.__class__.__name__}")
        m.print_metrics()

    return m


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

    with open("metrics.pkl", "wb") as f:
        pickle.dump(metrics_list, f)

    print("Saving plots...")
    for stat in stats:
        fig, axes = plt.subplots(1, 2, figsize=(15, 5))

        for i, dataset in enumerate(DATASET):
            plot_df(datasets_df[i], ax=axes[i], ylim=.8, ylab=stat)
            axes[i].set_title(f"{stat}@k for {dataset} dataset", fontsize=MEDIUM_SIZE)

        fig.savefig(f"{stat}@k.png")
