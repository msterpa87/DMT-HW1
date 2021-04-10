import csv

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
            ids = list(map(int, row[1][1:-1].replace(',','').split()))
            id_lists.append(ids)

    return id_lists


def count_duplicates(id_list):
    """ Return the number of exact duplicates song based on their shingles

    :param id_list: list of list of ints
        each element of the list represents the list of shingles ids of a song
    :return: int
        return the count of exact duplicates found
    """
    hashes = sorted([hash(tuple(x)) for x in id_list])

    duplicates = 0
    count = 1
    val = hashes[0]

    for i in range(1, len(hashes)):
        if hashes[i] != val:
            # compute duplicates of previous streak
            duplicates += int(count * (count - 1) / 2)
            val = hashes[i]
            count = 1
        else:
            count += 1

    return duplicates


if __name__ == "__main__":
    shingles_ids_list = load_shingles_id_from_tsv(TSV_FILENAME)
    n_duplicates = count_duplicates(shingles_ids_list)

    print(f"Found {n_duplicates} duplicates")
