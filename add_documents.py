from whoosh import index
from os import listdir
from bs4 import BeautifulSoup
from config import *


def id_from_filename(pathname):
    return re.search(r"([0-9]+)\.html", pathname).group(1)


def pathnames_from_dir(directory):
    files = list(filter(lambda x: 'html' in x, listdir(directory)))
    return list(map(lambda x: directory + x, files))


if __name__ == "__main__":
    # get index pathname from command line
    index_dir = target_path()

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