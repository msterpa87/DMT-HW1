from whoosh.qparser import *
from collections import defaultdict
from contextlib import suppress
import csv


def load_queries(pathname):
    """ Returns the list of queries contained in the target pathname tsv file

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
    """ Returns a dictionary of query_id: [results_ids]

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
    """ Computes the reciprocal rank of the two lists

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
    """ Filters the query for which there is a ground truth

    :param queries: dictionary of queries {query_id: string}
    :param gt: dictionary of ground truth results {query_id: list of ints}
    :return: dictionary of queries with a ground truth
    """
    filtered = {}

    for k,v in gt.items():
        with suppress(KeyError):
            filtered[k] = queries[k]

    return filtered


def mean_reciprocal_rank(ix, scoring_function, queries, results_gt):
    """ Returns the results of each query

    :param results_gt:
    :param ix: Whoosh index
    :param scoring_function: Whoosh scoring function
    :param queries: list of strings
    :return: dictionary {query_id: [results_ids]}
    """
    q_size = len(queries)
    cumulative_rank = 0

    with ix.searcher(weighting=scoring_function) as searcher:
        qp = QueryParser("content", ix.schema)

        for i, q in queries.items():
            # parse query
            parsed_query = qp.parse(q)

            # get results ids
            results = searcher.search(parsed_query)
            results_ids = list(map(lambda x: int(x['id']), results))

            # add reciprocal rank
            cumulative_rank += reciprocal_rank(results_ids, results_gt[i])

    return cumulative_rank / q_size