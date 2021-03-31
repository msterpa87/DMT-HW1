from whoosh import index
from whoosh.qparser import *
from whoosh import scoring
from build_index import INDEX_DIR
from collections import defaultdict


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


ix = index.open_dir(INDEX_DIR)
