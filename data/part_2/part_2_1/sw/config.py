import argparse

LYRICS_COL = 5
TITLE_COL = 1
SONGS_PATH = "../../dataset/250K_lyrics_from_MetroLyrics.csv"


def build_shingles_config():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, default=SONGS_PATH,
                        help="Input filename.tsv")
    parser.add_argument("-o", "--output", type=str, help="Output filename.tsv")
    parser.add_argument("-f", "--field", type=str, default="lyrics", choices=["lyrics", "title"],
                        help="Field to use to build shingles from songs tsv file")
    return parser.parse_args()
