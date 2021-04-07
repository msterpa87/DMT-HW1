import argparse
from whoosh import scoring
from whoosh.analysis import *
from utils import load_queries, load_ground_truth, queries_with_gt

INDEX_PATH = "data/part_1/index_"

# fill index with documents
CRANFIELD_DIR = "../Cranfield_DATASET/DOCUMENTS/"
TIME_DIR = "../Time_DATASET/DOCUMENTS/"

CRANFIELD_QUERY = "../Cranfield_DATASET/cran_Queries.tsv"
CRANFIELD_GT = "../Cranfield_DATASET/cran_Ground_Truth.tsv"
TIME_QUERY = "../Time_DATASET/time_Queries.tsv"
TIME_GT = "../Time_DATASET/time_Ground_Truth.tsv"

ANALYZERS = {'simple': SimpleAnalyzer(),
             'standard': StandardAnalyzer(),
             'stemming': StemmingAnalyzer(),
             'ngram_3': NgramAnalyzer(4)}

SCORINGS = {'frequency': scoring.Frequency(),
            'tfidf': scoring.TF_IDF(),
            'bm25f': scoring.BM25F}

K_VAL = [1, 3, 5, 10]


def load_dataset(dataset):
    """ Return a pair of dictionary keys the query_id and values
        respectively the string query and the list of ground truth ids
    
    :param dataset: a string in ['cranfield', 'time']
    :return: a pair [filtered_queries, queries_gt]
    """
    selection = {'cranfield': [CRANFIELD_QUERY, CRANFIELD_GT],
                 'time': [TIME_QUERY, TIME_GT]}

    # loading queries
    queries_path, gt_path = selection[dataset]
    queries = load_queries(queries_path)
    gt = load_ground_truth(gt_path)

    # keeping only queries with gt
    filtered_queries = queries_with_gt(queries, gt)

    return filtered_queries, gt


def query_config():
    """ Return a config dictionary with input parameters from command line

    :return: dictionary
    """
    # setting up command line parsing
    parser = argparse.ArgumentParser(description="Add documents to index")
    parser.add_argument('-a', '--analyzer', type=str, default='simple',
                        help=f"Choose analyzer among {ANALYZERS.keys()}")
    parser.add_argument('-s', '--scoring', type=str, default='frequency',
                        help=f"Choose scoring among {SCORINGS.keys()}")
    parser.add_argument('-d', '--dataset', type=str, default='cranfield',
                        help="Choose among ['cranfield', 'time']")
    parser.add_argument('-B', type=float, default=0.75, help="See BM25F documentation")
    parser.add_argument('-K1', type=float, default=1.2, help="See BM25F documentation")
    args = parser.parse_args()

    config = {'path': INDEX_PATH + args.dir,
              'scoring': SCORINGS[args.scoring],
              'dataset': args.dataset}

    # set custom parameters for BM25F
    if args.scoring == 'bm25f':
        config['scoring'] = config['scoring'](B=args.B, K1=args.K1)

    return config


def selected_analyzer():
    """ Return the selected analyzer from command line

    :return: str
    """
    parser = argparse.ArgumentParser(description="Build index")
    parser.add_argument('-a', '--analyzer', default='simple',
                        type=str, help=f"Choose among {list(ANALYZERS.keys())}")
    args = parser.parse_args()

    return args.analyzer
