from utils import *


if __name__ == "__main__":
    # read parameters from command line
    args = build_shingles_config()

    print(f"Reading shingles from {args.input}")
    songs_list = shingles_from_tsv(field=args.field)

    print(f"Creating shingle id dictionary for {len(songs_list)} shingles")
    shingles_ids = shingles_id_from_list(songs_list)

    print("Translating shingles list to list of shingles identifiers.")
    songs_shingles_ids_list = []

    for song in tqdm(songs_list):
        shingles_list = song.get_shingles()
        songs_shingles_ids_list.append(shingles_as_list(shingles_ids, shingles_list))

    print(f"Writing shingles to {args.output}")

    with open(args.output, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')
        writer.writerow(["ID", "ELEMENTS_IDS"])

        for i, song in tqdm(enumerate(songs_list)):
            song_id = song.get_id()
            id_list = songs_shingles_ids_list[i]

            # save to file non-empty lists
            if len(id_list) > 0:
                writer.writerow([f"id_{song_id}", id_list])
