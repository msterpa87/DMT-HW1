from utils import *

SHINGLES_FILENAME = "shingles.tsv"

if __name__ == "__main__":
    print(f"Reading shingles from {SONGS_PATH}")
    lyrics_shingles = shingles_from_lyrics()

    print(f"Creating shingle id dictionary for {len(lyrics_shingles)} lyrics")
    shingle_id = shingles_id_from_list(lyrics_shingles)

    lyrics_id_lists = []

    print("Getting list identifiers.")
    for i in tqdm(range(len(lyrics_shingles))):
        lyrics_id_lists.append(shingles_as_list(shingle_id, lyrics_shingles[i]))

    print("Writing shingles to ")
    with open(SHINGLES_FILENAME, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')
        writer.writerow(["ID", "ELEMENTS_IDS"])

        for i, id_list in enumerate(lyrics_id_lists):
            writer.writerow([f"id_{i}", id_list])
