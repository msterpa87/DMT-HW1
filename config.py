import argparse
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


def target_path():
    """ Return the full pathname of the selected index

    :return: str
    """

    parser = argparse.ArgumentParser(description="Add documents to index")
    parser.add_argument('--dir', type=str, help=f"Choose among {ANALYZERS.keys()}")
    args = parser.parse_args()

    return INDEX_PATH + args.dir


def selected_analyzer():
    parser = argparse.ArgumentParser(description="Build index")
    parser.add_argument('-a', '--analyzer', default='simple',
                        type=str, help=f"Choose among {list(ANALYZERS.keys())}")
    args = parser.parse_args()

    return args.analyzer
