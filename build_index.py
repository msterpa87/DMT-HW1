from whoosh.fields import Schema, TEXT, ID
from whoosh.index import create_in
import os.path
from config import *


if __name__ == "__main__":
    analyzer_str = selected_analyzer()

    index_dir = INDEX_PATH + analyzer_str
    analyzer = ANALYZERS[analyzer_str]

    # create index directory
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)

    # define schema
    schema = Schema(id=ID(stored=True),
                    content=TEXT(stored=False, analyzer=analyzer))

    create_in(index_dir, schema)