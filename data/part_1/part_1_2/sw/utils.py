from collections import defaultdict
from contextlib import suppress
import csv
import numpy as np


def load_queries_results(pathname):
    """ Returns a dictionary of query_id: [results_ids]

    :param pathname: string
    :return: dictionary {query_id: list of ids}
        list of ids is sorted by rank
    """
    results = defaultdict(list)

    with open(pathname) as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')

        # skip header
        next(reader, None)

        for query_id, doc_id, rank in reader:
            results[int(query_id)].append([int(doc_id), int(rank)])

    # sort by rank and drop it
    for query_id, doc_id in results.items():
        results[query_id] = [x[0] for x in sorted(doc_id, key=lambda x: x[1])]

    return results


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

        for query_id, doc_id in reader:
            queries_gt[int(query_id)].append(int(doc_id))

    return queries_gt


def queries_with_gt(queries, gt):
    """ Filters the query for which there is a ground truth

    :param queries: dictionary of queries {query_id: string}
    :param gt: dictionary of ground truth results {query_id: list of ints}
    :return: dictionary of queries with a ground truth
    """
    filtered = {}

    for query_id in gt.keys():
        with suppress(KeyError):
            filtered[query_id] = queries[query_id]

    return filtered


def recall_at_k(results_ids, results_gt, k=None):
    """ Returns the dictionary of R-precision for each query

    :param results_ids: dictionary {query_id: [list of ids]}
    :param results_gt: dictionary {query_id: [list of ids]}
    :param k: int
        if None is equivalent to computing the R-Precision by considering
        all relevant documents returned
    :return: dictionary {query_id: r-precision}
    """
    recall_dict = dict()

    for query_id, docs_id in results_ids.items():
        # current ground truth
        gt = results_gt[query_id]

        if k is None:
            k = len(docs_id)

        # handle case of number of gt ids < k
        k = min(k, len(gt))

        # compute recall
        relevant_returned = len(list(set(gt).intersection(set(docs_id[:k]))))
        total_relevant = len(gt)
        recall_dict[query_id] = relevant_returned / total_relevant

    return recall_dict


def precision_at_k(results_ids, results_gt, k):
    """ Returns the dictionary of R-precision for each query

    :param results_ids: dictionary {query_id: [list of ids]}
    :param results_gt: dictionary {query_id: [list of ids]}
    :param k: int
    :return: dictionary {query_id: r-precision}
    """
    precision_dict = dict()

    for query_id, docs_id in results_ids.items():
        # current ground truth
        gt = results_gt[query_id]

        # handle case of number of gt ids < k
        k = min(k, len(gt))

        docs_id = docs_id[:k]

        relevant_returned = len(list(set(gt).intersection(set(docs_id))))
        precision_dict[query_id] = relevant_returned / k

    return precision_dict


def compute_stats(d):
    """ Return a dictionary of aggregate stats on d

    :param d: dictionary {int: float}
        expects a dictionary of {query_id: value} returned from either
        precision_at_k or recall_at_k
    :return: dictionary {string: float}
    """
    vals = list(d.values())

    stats = {'min': np.min(vals),
             'max': np.max(vals),
             'mean': np.mean(vals),
             'median': np.median(vals),
             'first_quartile': np.quantile(vals, 0.25),
             'third_quartile': np.quantile(vals, 0.75)}

    return stats


def print_stats(stats_list, title):
    """ Prints to console the aggregate stats given as input

    :param stats_list: list of dictionary
        a dictionary is the output of compute_stats()
    :return: None
    """
    print(title)
    print(f"Search Engine stats:")
    print("N\t" + "\t".join(stats_list[0].keys()))

    for i, stats in enumerate(stats_list):
        values = list(stats.values())
        string = f"{i + 1}\t" + "\t".join(format(x, ".2f") for x in values[:-1]) + \
                 "\t\t" + format(values[-1], ".2f")
        print(string)

    print()


def fscore_from_pr(precision, recall):
    """

    :param precision:
    :param recall:
    :return:
    """
    precision = np.array(list(precision.values()))
    recall = np.array(list(recall.values()))
    np.seterr(all="ignore")
    fscore = (2 * precision * recall) / (precision + recall)

    return fscore[~np.isnan(fscore)].mean()


def print_fscore(fscore):
    """

    :param fscore:
    :return:
    """
    print("F-score:")
    print("\t".join(map(str, range(1, len(fscore)+1))))
    print("\t".join([format(x, ".2f") for x in fscore]))
