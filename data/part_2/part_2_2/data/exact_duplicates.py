import csv
from collections import defaultdict
from time import time

TSV_FILENAME = "./title_shingles.tsv"


def load_shingles_id_from_tsv(filename):
    """

    :param filename: string
        filename containing the shingles generated from build_shingles.py
        first row is the header, the remaining rows are made of "song_id [shingle_ids]"
    :return:
    """
    id_lists = []

    with open(filename, "r") as f:
        reader = csv.reader(f, delimiter='\t')
        next(reader)

        for row in reader:
            ids = list(map(int, row[1][1:-1].replace(',', '').split()))
            id_lists.append(ids)

    return id_lists


def count_duplicates(id_list):
    """ Return the number of exact duplicates song based on their shingles

    :param id_list: list of list of ints
        each element of the list represents the list of shingles ids of a song
    :return: int
        return the count of exact duplicates found
    """
    shingles_dict = defaultdict(int)

    for s in id_list:
        # cast to tuple to compute hash
        t = tuple(s)
        # increase duplicates count for shingle
        shingles_dict[hash(t)] += 1

    return sum(list(map(lambda n: int(n*(n-1)/2), shingles_dict.values())))


if __name__ == "__main__":
    tic = time()
    shingles_ids_list = load_shingles_id_from_tsv(TSV_FILENAME)
    n_duplicates = count_duplicates(shingles_ids_list)

    elapsed = (time() - tic)

    print(f"Found {n_duplicates} duplicates in {elapsed:.2f} seconds")
