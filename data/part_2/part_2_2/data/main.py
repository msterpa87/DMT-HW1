import csv
from collections import defaultdict
from time import time
from tqdm import tqdm

TSV_FILENAME = "./title_shingles.tsv"


def load_shingles_id_from_tsv(filename):
    """ Returns a list of identifier associated to the shingles from filename

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


def count_duplicates(duplicates_list):
    """ Return the number of exact duplicates song based on their shingles

    :param duplicates_list: list of list of ints
        each element of the list represents the list of shingles ids of a song
    :return: int
        return the count of exact duplicates found
    """
    return sum(list(map(lambda d_list: int(len(d_list) * (len(d_list)-1)/2), duplicates_list.values())))


def find_duplicates(id_list):
    """ Return the list of pairs of duplicates found

    :param id_list: list of list of ints
        each element of the list represents the list of shingles ids of a song
    :return: int
        return the count of exact duplicates found
    """
    shingles_dict = defaultdict(list)

    for i, s in enumerate(id_list):
        # cast to tuple to compute hash
        t = tuple(s)
        # increase duplicates count for shingle
        shingles_dict[hash(t)].append(i)

    return shingles_dict


def duplicates_to_tsv(duplicates):
    """ Saves duplicates to tsv file

    :param duplicates: dict {id: list of ints}
        a dictionary with hash as key and list of doc_ids as values
    """
    with open("exact_duplicates.tsv", "w", newline='') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(["id_set_1", "id_set_2"])

        for duplicate_group in duplicates.values():
            for i, id_1 in enumerate(duplicate_group[:-1]):
                for id_2 in duplicate_group[i+1:]:
                    writer.writerow([id_1, id_2])


if __name__ == "__main__":
    tic = time()

    # load shingles
    shingles_ids_list = load_shingles_id_from_tsv(TSV_FILENAME)

    # find exact duplicates
    duplicates = find_duplicates(shingles_ids_list)
    n_duplicates = count_duplicates(duplicates)

    elapsed = (time() - tic)

    print(f"Found {n_duplicates} duplicates in {elapsed:.2f} seconds")

    # save to tsv file
    print("Saving duplicates to tsv file...")
    duplicates_to_tsv(duplicates)