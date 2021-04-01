from whoosh import index
from build_index import INDEX_DIR
from os import listdir
from bs4 import BeautifulSoup
import re

# fill index with documents
CRANFIELD_DIR = "data/part_1/part_1_1/Cranfield_DATASET/DOCUMENTS/"
TIME_DIR = "data/part_1/part_1_1/Time_DATASET/DOCUMENTS/"


def id_from_filename(pathname):
    return re.search(r"([0-9]+)\.html", pathname).group(1)


def pathnames_from_dir(directory):
    files = list(filter(lambda x: 'html' in x, listdir(directory)))
    return list(map(lambda x: directory + x, files))


if __name__ == "__main__":
    # open index
    ix = index.open_dir(INDEX_DIR)
    writer = ix.writer()

    files = pathnames_from_dir(CRANFIELD_DIR) + pathnames_from_dir(TIME_DIR)

    for pathname in files:
        #print(f"[{pathname}]")
        # read html content
        with open(pathname, "r") as file:
            html = file.read()

        soup = BeautifulSoup(html, "html.parser")

        # add document to index
        doc_id = id_from_filename(pathname)
        # title = soup.title.string.strip()
        content = soup.body.string.strip()
        writer.add_document(id=doc_id, content=content)

    writer.commit()

    print(f"Added {len(files)} documents")