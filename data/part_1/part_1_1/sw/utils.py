from whoosh.qparser import *
from collections import defaultdict
from contextlib import suppress
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import csv

sns.set_theme()

K_VAL = [1, 3, 5, 10]


class Metrics(object):
    def __init__(self, index_type, dataset, scoring_function):
        self.scoring_function = scoring_function
        self.dataset = dataset
        self.index_type = index_type
        self.MRR = None
        self.rp = None
        self.rps = None
        self.rp_at_k = None
        self.ndcg_at_k = None

    def compute_metrics(self, results_ids, queries_gt):
        """ Given the query results and the ground truth computes
            several metrics (MRR, Precision, etc.)

        :param results_ids: dictionary
            has the structure {query_id: list of doc_ids}
        :param queries_gt: dictionary
        :return:
        """
        # compute metrics
        self.MRR = mean_reciprocal_rank(results_ids, queries_gt)

        # compute R-precision
        self.rp = recall_at_k(results_ids, queries_gt)
        self.rps = compute_stats(self.rp)

        # Precision at k plot
        self.rp_at_k = [compute_stats(precision_at_k(results_ids, queries_gt, k))['mean'] for k in K_VAL]

        # Normalized Discounted Cumulative Gain at k plot
        self.ndcg_at_k = [mean_ndcg(results_ids, queries_gt, k) for k in K_VAL]

    def print_metrics(self):
        """ Print to console the metrics computed """

        lines = [f"P@k {self.rp_at_k}",
                 f"NDCG@k {self.ndcg_at_k}",
                 f"MRR: {self.MRR}",
                 "[R-Precision]",
                 f"Mean: \t\t {self.rps['mean']}",
                 f"Min: \t\t {self.rps['min']}",
                 f"1st quartile:\t {self.rps['first_quartile']}",
                 f"Median: \t {self.rps['median']}",
                 f"3rd quartile:\t {self.rps['third_quartile']}",
                 f"Max:\t\t {self.rps['max']}",
                 "\n" + "="*20 + "\n"]
        print("\n".join(lines))

    def __str__(self):
        return f"{self.index_type}-{self.scoring_function}"


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

        for k, v in reader:
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
    :param queries: list of strings
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


def recall_at_k(results_ids, results_gt, k=None):
    """ Returns a dictionary representing the recall at k

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
            k = len(gt)

        # compute recall
        relevant_returned = len(list(set(gt).intersection(set(docs_id[:k]))))
        total_relevant = len(gt)
        recall_dict[query_id] = relevant_returned / total_relevant

    return recall_dict


def precision_at_k(results_ids, results_gt, k=None):
    """ Returns the dictionary of R-precision for each query

    :param results_ids: dictionary {query_id: [list of ids]}
    :param results_gt: dictionary {query_id: [list of ids]}
    :param k: int
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
        rp[i] = r / k

    return rp


def compute_stats(rp):
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


def normalized_dcg(results_ids, results_gt, k=None):
    """ Return the discounted cumulative gain

    :param results_ids: list of ints
    :param results_gt: list of ints
    :param k: int
    :return: float
    """
    total = 0.0

    if k is None:
        k = min(len(results_ids), k)

    # normalization factor wrt gt
    norm = 1 + sum(map(lambda x: 1 / np.log2(x + 1), range(1, k)))

    for i in range(k):
        # binary relevance (1 if in gt, 0 otherwise)
        rel = int(results_ids[i] in results_gt)
        den = 1 if i == 0 else np.log2(i+1)
        total += (rel / den)

    return total / norm


def mean_ndcg(results_ids, results_gt, k):
    """ Returns the average normalized DCG

    :param results_ids: list of list of ints
    :param results_gt: list of list of ints
    :param k: int
    :return: float
    """
    totals = [normalized_dcg(results_ids[i], results_gt[i], k) for i in results_ids.keys()]
    return sum(totals) / len(totals)


def dataframe_from_metrics(metrics_list):
    """ Returns a dataframe of metrics, used for plotting

    :param metrics_list: list of Metrics objects
    :return: pandas.DataFrame
    """
    top5_metrics = metrics_list[:5]
    k_vals = [1, 3, 5, 10]

    metrics_str = []
    precisions = []
    ncdg = []

    for m in top5_metrics:
        metrics_str += [str(m)] * 4
        precisions += m.rp_at_k
        ncdg += m.ndcg_at_k

    df = pd.DataFrame.from_dict({'k': k_vals * 5,
                                 'metric': metrics_str,
                                 'precision': precisions,
                                 'ncdg': ncdg})

    return df


def plot_df(df, ax, ylab, ylim, legend_title="Preprocess-scoring"):
    """ Create a barplot from the metrics contained in the input DataFrame

    :param df: pandas.DataFrame
    :param ax: matplotlib.Axes
    :param ylab: string
    :param ylim: int
    :param legend_title: string
    :return:
    """
    plt.figure(figsize=(10, 8))
    scatter = sns.barplot(data=df, ax=ax, x="k", y=ylab, hue="metric")
    scatter.legend(title=legend_title)
    scatter.set(ylim=(0, ylim))
