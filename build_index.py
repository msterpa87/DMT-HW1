from whoosh.fields import Schema, TEXT, ID
from whoosh.index import create_in
from whoosh.analysis import SimpleAnalyzer
import os.path

INDEX_DIR = "data/part_1/indexdir"

# create index directory
if not os.path.exists(INDEX_DIR):
    os.mkdir(INDEX_DIR)

# define analyzer
analyzer = SimpleAnalyzer()

# define schema
schema = Schema(id=ID(stored=True),
                content=TEXT(stored=False, analyzer=analyzer))

create_in(INDEX_DIR, schema)