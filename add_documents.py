from whoosh import index
from make_index import INDEX_DIR
from os import listdir
from bs4 import BeautifulSoup
import re
from tqdm import tqdm

# fill index with documents
CRANFIELD_DIR = "data/part_1/part_1_1/Cranfield_DATASET/DOCUMENTS/"
TIME_DIR = "data/part_1/part_1_1/Time_DATASET/DOCUMENTS/"


def id_from_filename(pathname):
    return re.search(r"([0-9]+)\.html", pathname).group(1)


def add_documents_from_dir(writer, directory):
    """
        Add to the index all the documents inside directory
    :param writer: Whoosh index writer object
    :param directory: pathname of target directory
    """
    # add docs from cranfield dataset
    for filename in listdir(directory):
        pathname = directory + filename
        print(f"[{pathname}]")
        add_document_from_pathname(writer, pathname)


def add_document_from_pathname(writer, pathname):
    """
        Adds a document to the index

    :param writer: Whoosh index writer object
    :param pathname: pathname to html document
    """
    # read html content
    with open(pathname, "r") as file:
        html = file.read()

    soup = BeautifulSoup(html, "html.parser")

    # add document to index
    doc_id = id_from_filename(pathname)
    title = soup.title.string.strip()
    content = soup.body.string.strip()
    writer.add_document(title=title, id=doc_id, content=content)


if __name__ == "__main__":
    # open index
    ix = index.open_dir(INDEX_DIR)
    writer = ix.writer()

    add_documents_from_dir(writer, CRANFIELD_DIR)
    add_documents_from_dir(writer, TIME_DIR)

    writer.commit()
