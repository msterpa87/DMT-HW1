from whoosh.qparser import *
from collections import defaultdict
from contextlib import suppress
import csv
import numpy as np


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


def get_results_ids(ix, scoring_function, queries):
    """ Returns a dictionary containing a list of documents ids for each query

    :param ix: Whoosh index
    :param scoring_function: Whoosh scoring function
    :param queries:
    :return:
    """
    results_ids = {}

    with ix.searcher(weighting=scoring_function) as searcher:
        qp = QueryParser("content", ix.schema)

        for i, q in queries.items():
            # parse query
            parsed_query = qp.parse(q)

            # get results ids
            results = searcher.search(parsed_query)
            results_ids[i] = list(map(lambda x: int(x['id']), results))

    return results_ids


def r_precision(results_ids, results_gt, k=None):
    """ Returns the dictionary of R-precision for each query

    :param results_ids: dictionary {query_id: [list of ids]}
    :param results_gt: dictionary {query_id: [list of ids]}
    :param k:
    :return: dictionary {query_id: r-precision}
    """
    rp = {}

    for i, ids in results_ids.items():
        # current ground truth
        gt = results_gt[i]
        size = len(gt)

        # consider the first len(gt) documents
        if k is None:
            k = size

        ids = ids[:k]

        r = len(list(set(gt).intersection(set(ids))))
        rp[i] = r / size

    return rp


def r_precision_stats(rp):
    """ Return a dictionary of stats on R-Precision

    :param rp: dictionary {query_id: float}
    :return: dictionary {string: float}
    """
    vals = list(rp.values())
    stats = {'min': np.min(vals),
             'max': np.max(vals),
             'mean': np.mean(vals),
             'median': np.median(vals),
             'first_quartile': np.quantile(vals, 0.25),
             'third_quartile': np.quantile(vals, 0.75)}

    return stats


def mean_reciprocal_rank(results_ids, results_gt):
    """ Compute the mean reciprocal rank

    :param results_ids: dictionary {query_id: [list of ids]}
    :param results_gt: dictionary {query_id: [list of ids]}
    :return: dictionary {query_id: [results_ids]}
    """
    q_size = len(results_ids)
    cumulative_rank = 0

    for i, ids in results_ids.items():

        # add reciprocal rank
        cumulative_rank += reciprocal_rank(ids, results_gt[i])

    return cumulative_rank / q_size


def ndcg(results_ids, results_gt, k=None):
    """ Return the discounted cumulative gain

    :param results_ids: list of ints
    :param results_gt: list of ints
    :param k: int
    :return: float
    """
    total = 0.0

    # normalization factor wrt gt
    norm = 1 + sum(map(lambda x: 1 / np.log2(x + 1), range(1, len(results_gt))))

    if k is None:
        k = min(len(results_ids), k)

    for i in range(k):
        # binary relevance (1 if in gt, 0 otherwise)
        rel = int(results_ids[i] in results_gt)
        den = 1 if i == 0 else np.log2(i+1)
        total = total + (rel / den)

    return total / norm


def mean_ndcg(results_ids, results_gt, k):
    """

    :param results_ids:
    :param results_gt:
    :param k:
    :return:
    """
    totals = [ndcg(results_ids[i], results_gt[i], k) for i in results_ids.keys()]
    return sum(totals) / len(totals)