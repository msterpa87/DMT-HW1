from utils import *


if __name__ == "__main__":
    # read parameters from command line
    args = config()

    print(f"Reading shingles from {args.input}")

    shingles = shingles_from_tsv(col=args.col)

    print(f"Creating shingle id dictionary for {len(shingles)} shingles")

    shingle_id = shingles_id_from_list(shingles)

    id_lists = []

    print("Getting identifiers list.")

    for i in tqdm(range(len(shingles))):
        id_lists.append(shingles_as_list(shingle_id, shingles[i]))

    print(f"Writing shingles to {args.output}")

    with open(args.output, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')
        writer.writerow(["ID", "ELEMENTS_IDS"])

        for i, id_list in enumerate(id_lists):
            # save to file non-empty lists
            if len(id_list) > 0:
                writer.writerow([f"id_{i}", id_list])
