import argparse
from whoosh import scoring
from whoosh.analysis import *

INDEX_PATH = "data/part_1/index_"

# fill index with documents
CRANFIELD_DIR = "data/part_1/part_1_1/Cranfield_DATASET/DOCUMENTS/"
TIME_DIR = "data/part_1/part_1_1/Time_DATASET/DOCUMENTS/"

CRANFIELD_QUERY = "data/part_1/part_1_1/Cranfield_DATASET/cran_Queries.tsv"
CRANFIELD_GT = "data/part_1/part_1_1/Cranfield_DATASET/cran_Ground_Truth.tsv"
TIME_QUERY = "data/part_1/part_1_1/Time_DATASET/time_Queries.tsv"
TIME_GT = "data/part_1/part_1_1/Time_DATASET/time_Ground_Truth.tsv"

ANALYZERS = {'simple': SimpleAnalyzer(),
             'standard': StandardAnalyzer(),
             'stemming': StemmingAnalyzer(),
             'ngram_3': NgramAnalyzer(4)}

SCORINGS = {'frequency': scoring.Frequency(),
            'tfidf': scoring.TF_IDF(),
            'bm25f': scoring.BM25F}


def query_config():
    """ Return a config dictionary with input parameters from command line

    :return: dictionary
    """
    # setting up command line parsing
    parser = argparse.ArgumentParser(description="Add documents to index")
    parser.add_argument('-d', '--dir', type=str, default='simple',
                        help=f"Choose analyzer among {ANALYZERS.keys()}")
    parser.add_argument('-s', '--scoring', type=str, default='frequency',
                        help=f"Choose scoring among {SCORINGS.keys()}")
    parser.add_argument('-B', type=float, default=0.75, help="See BM25F documentation")
    parser.add_argument('-K1', type=float, default=1.2, help="See BM25F documentation")
    args = parser.parse_args()

    config = {'path': INDEX_PATH + args.dir,
              'scoring': SCORINGS[args.scoring]}

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
