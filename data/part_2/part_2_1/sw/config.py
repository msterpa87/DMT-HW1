import argparse

LYRICS_COL = 5
TITLE_COL = 1
SONGS_PATH = "../../dataset/250K_lyrics_from_MetroLyrics.csv"


def analysis_config():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--ground-truth", type=str, default="./BRUTE_FORCE_near_duplicates.tsv")
    parser.add_argument("-p", "--pred", type=str, default="./PRED_near_duplicates.tsv")
    return parser.parse_args()


def build_shingles_config():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, default=SONGS_PATH,
                        help="Input filename.tsv")
    parser.add_argument("-o", "--output", type=str, help="Output filename.tsv")
    return parser.parse_args()
