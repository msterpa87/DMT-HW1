import csv
import string
from tqdm import tqdm
from itertools import chain

translate_table = dict((ord(char), None) for char in string.punctuation)
LYRICS_COL = 5
SONGS_PATH = "../../dataset/250K_lyrics_from_MetroLyrics.csv"


def preprocess(s):
    """ Remove punctuation and lower case the string

    :param s: string
    :return: string
    """
    s = s.translate(translate_table)
    return s.lower()


def shingles(s, length=3):
    """ Computes the length-shingles of the string s

    :param s: string
    :param length: int
        size of a shingle (number of tokens from the string)
    :return: list of lists of strings
    """
    tokens = s.split()
    if len(tokens) < 3:
        return []

    return [tuple(tokens[i:i + length]) for i in range(len(tokens) - (length-1))]


def shingles_from_lyrics():
    """ Returns a list where each element is a list of shingles of one of the lyrics

    :return: nested list of strings
        [[[s1,s2,s3], ...], ...]
    """
    lyrics_shingles = []

    with open(SONGS_PATH) as f:
        # open csv file and skip header
        reader = csv.reader(f)
        next(reader)

        # iterate over rows
        for row in tqdm(reader):
            lyrics = preprocess(row[LYRICS_COL])
            lyrics_shingles.append(shingles(lyrics))

    return lyrics_shingles


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
