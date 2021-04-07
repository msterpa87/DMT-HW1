from whoosh.fields import Schema, TEXT, ID
from whoosh.index import create_in
from whoosh import index
import os
from config import *
from bs4 import BeautifulSoup


def id_from_filename(pathname):
    return re.search(r"([0-9]+)\.html", pathname).group(1)


def pathnames_from_dir(directory):
    files = list(filter(lambda x: 'html' in x, os.listdir(directory)))
    return list(map(lambda x: directory + x, files))


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

    # create index
    create_in(index_dir, schema)

    # open index
    ix = index.open_dir(index_dir)
    writer = ix.writer()

    files = pathnames_from_dir(CRANFIELD_DIR) + pathnames_from_dir(TIME_DIR)

    for pathname in files:
        # read html content
        with open(pathname, "r") as file:
            html = file.read()

        soup = BeautifulSoup(html, "html.parser")

        # add document to index
        doc_id = id_from_filename(pathname)
        content = soup.body.string.strip()
        writer.add_document(id=doc_id, content=content)

    writer.commit()

    print(f"Added {len(files)} documents")
