import csv
import string
from tqdm import tqdm
from itertools import chain
from collections import defaultdict
from config import *

translate_table = dict((ord(char), None) for char in string.punctuation.replace("'", ""))


##########################################
# FUNCTIONS TO CREATE SHINGLES TSV FILES #
##########################################

def preprocess(s, remove_dash=False):
    """ Remove punctuation and lower case the string

    :param s: string
    :param remove_dash: bool
    :return: string
    """
    if remove_dash:
        s = s.replace("-", " ")

    s = s.translate(translate_table)
    return s.lower()


def get_shingles(s, length=3, keep_short=False):
    """ Computes the length-shingles of the string s

    :param s: string
        input string from which to build the shingles
    :param length: int
        size of a shingle (number of tokens from the string)
    :param keep_short: bool
        return a whole shingle even if there are less than length words
    :return: list of lists of strings
        list of all shingles generated
    """
    tokens = s.split()
    if len(tokens) < 3:
        if keep_short:
            return [tuple(tokens)]
        else:
            return []

    return [tuple(tokens[i:i + length]) for i in range(len(tokens) - (length-1))]


def shingles_from_tsv(col=LYRICS_COL):
    """ Returns a list where each element is a list of shingles of one of the lyrics

    :return: nested list of strings
        [[[s1,s2,s3], ...], ...]
    """
    shingles_list = []

    remove_dash = False
    keep_short = False

    if col != LYRICS_COL:
        remove_dash = True
        keep_short = True

    with open(SONGS_PATH) as f:
        # open csv file and skip header
        reader = csv.reader(f)
        next(reader)

        # iterate over rows
        for row in tqdm(reader):
            shingles = preprocess(row[col], remove_dash=remove_dash)
            shingles_list.append(get_shingles(shingles, keep_short=keep_short))

    return shingles_list


def shingles_id_from_list(lyrics_shingles):
    """ Assigns a unique identifier to each shingle

    :param lyrics_shingles: nested list of shingles
        a list of list of lists of 3 strings, the direct output of shingles_from_lyrics()
    :return: dictionary {tuple: int}
        a dictionary {shingle: id}
    """
    unique_shingles = list(set(chain(*lyrics_shingles)))
    return dict(zip(unique_shingles, range(len(unique_shingles))))


def shingles_as_vector(id_dict, shingles_list):
    """ Computes the indicator vector of shingle_list according to the identifier in id_dict

    :param id_dict: dictionary {tuple of 3 strings: int}
    :param shingles_list: list of tuple of 3 strings
    :return: list of ints
        v[i] = 1 iff shingle_i is in shingles_list
    """
    n_id = len(id_dict)
    vector = [0] * n_id

    for shingle in shingles_list:
        vector[id_dict[shingle]] = 1

    return vector


def shingles_as_list(id_dict, shingle_list):
    """ Returns a list the (unique) identifiers contained in shingle_list

    :param id_dict: dictionary {tuple of 3 strings: int}
    :param shingle_list: list of tuple of 3 strings
    :return: list of ints
    """
    return sorted(list(set([id_dict[s] for s in shingle_list])))


#########################################################
# FUNCTIONS TO LOAD OUTPUT OF NEAR DUPLICATES DETECTION #
#########################################################

def load_near_duplicates_tsv(pathname):
    """ Loads the output of the near duplicate detection algorithm
        in a dictionary that contains the jaccard similarities of
        all the sets ordered by id

    :param pathname: string
        full pathname of tsv file output by near duplicate detection class
    :return: nested dictionary
        return a dictionary where dict[id_1][id_2] = jaccard_similarity(id_1, id_2)
    """
    near_duplicates = defaultdict(dict)

    with open(pathname, "r") as f:
        reader = csv.reader(f, delimiter='\t')
        next(reader)

        for line in reader:
            jaccard, id_1, _, id_2, _ = line
            near_duplicates[int(id_1)][int(id_2)] = float(jaccard)

    return near_duplicates


def near_duplicates_stats(gt, pred):
    """ Returns detection probability, number of false positives and negatives

    :param gt: dictionary
        output of load_near_duplicates_tsv()
    :param pred: dictionary
        output of load_near_duplicates_tsv()
    :return: float, int, int
        1. detection probability = detected_pairs / ground_truth_pairs
        2. false positives
        3. false negatives
    """
    total_near_duplicates = 0
    total_detected = 0
    false_negatives = 0
    false_positives = 0

    for id_1, nd_dict in gt.items():
        # sum ground truth near duplicates of id_1
        total_near_duplicates += len(nd_dict)

        # sum detected and false positives near duplicates
        for id_2 in nd_dict.keys():
            if int(id_2 in pred[id_1] or id_1 in pred[id_2]):
                total_detected += 1
            else:
                false_negatives += 1

    for id_1, nd_dict in pred.items():
        for id_2 in nd_dict.keys():
            false_positives += int(id_1 not in gt[id_2] and id_2 not in gt[id_1])

    detection_prob = total_detected / total_near_duplicates

    return detection_prob, false_positives, false_negatives
