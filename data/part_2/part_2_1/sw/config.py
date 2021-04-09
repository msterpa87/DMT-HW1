import argparse

LYRICS_COL = 5
TITLE_COL = 1
SONGS_PATH = "../../dataset/250K_lyrics_from_MetroLyrics.csv"


def config():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, default=SONGS_PATH,
                        help="Input filename.tsv")
    parser.add_argument("-o", "--output", type=str, help="Output filename.tsv")
    parser.add_argument("-c", "--col", type=int, default=LYRICS_COL,
                        help="Column to use to build shingles in songs tsv file")
    parser.add_argument("--keep_short", type=bool, default=False,
                        help="Keep shingles shorter than 3")
    return parser.parse_args()
