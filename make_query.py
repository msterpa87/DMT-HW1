from whoosh import index
from whoosh.qparser import *
from whoosh import scoring
from build_index import INDEX_DIR
from collections import defaultdict
from contextlib import suppress
import csv

CRANFIELD_QUERY = "data/part_1/part_1_1/Cranfield_DATASET/cran_Queries.tsv"
CRANFIELD_GT = "data/part_1/part_1_1/Cranfield_DATASET/cran_Ground_Truth.tsv"
TIME_QUERY = "data/part_1/part_1_1/Time_DATASET/time_Queries.tsv"
TIME_GT = "data/part_1/part_1_1/Time_DATASET/time_Ground_Truth.tsv"


def load_queries(pathname):
    """
        Returns the list of queries contained in the target pathname tsv file

    :param pathname: string
    :return: dictionary {query_id: string}
    """
    queries = {}

    with open(pathname) as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')

        # skip header
        next(reader, None)

        for k,v in reader:
            queries[int(k)-1] = v

    return queries


def load_ground_truth(pathname):
    """
        Returns a dictionary of query_id: [results_ids]

    :param pathname: string
    :return: dictionary {query_id: list of ids}, ids as int
    """
    queries_gt = defaultdict(list)

    with open(pathname) as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')

        # skip header
        next(reader, None)

        for k, v in reader:
            queries_gt[int(k) - 1].append(int(v))

    return queries_gt


def reciprocal_rank(result, gt):
    """

    :param result: set of ints
    :param gt: set of ints
    :return: reciprocal rank of
    """
    common = list(set.intersection(set(result), set(gt)))

    # 0 if no relevant query
    if len(common) == 0:
        return 0

    # first relevant query
    rank = min(list(map(lambda x: result.index(x), common))) + 1

    return 1 / rank


def queries_with_gt(queries, gt):
    """
        Filters the query for which there is a ground truth

    :param queries: dictionary of queries {query_id: string}
    :param gt: dictionary of ground truth results {query_id: list of ints}
    :return: dictionary of queries with a ground truth
    """
    filtered = {}

    for k,v in enumerate(gt):
        with suppress(KeyError):
            filtered[k] = queries[k]

    return filtered


def make_multiple_queries(ix, scoring_function, queries):
    """
        Returns the results of each query

    :param ix: Whoosh index
    :param scoring_function: Whoosh scoring function
    :param queries: list of strings
    :return: dictionary {query_id: [results_ids]}
    """



if __name__ == "__main__":
    ix = index.open_dir(INDEX_DIR)

    # loading queries
    cranfield_queries = load_queries(CRANFIELD_QUERY)
    time_queries = load_queries(TIME_QUERY)

    # loading ground truth
    cranfield_gt = load_ground_truth(CRANFIELD_GT)
    time_gt = load_ground_truth(TIME_GT)

    qp = QueryParser("content", ix.schema)

    # (!) we should implement up to 12 different configurations here
    scoring_function = scoring.Frequency()

    cumulative_rank = 0

    #filtered_cranfield = list(map(lambda))

    for query_id, gt_ids in cranfield_gt:
        parsed_query = qp.parse(q)
        searcher = ix.searcher(weighting=scoring_function)
        results = searcher.search(parsed_query)

        # compare query results with ground truth and compute rank
        results_ids = list(map(lambda x: int(x['id']), results))
        gt_ids = cranfield_gt[i]
        cumulative_rank += reciprocal_rank(results_ids, gt_ids)

    # ADD SAME LOOP FOR TIME QUERIES AND THEN COMPUTE MRR