from whoosh.fields import Schema, TEXT, ID
from whoosh.index import create_in
from whoosh import index
import os
from config import *
from bs4 import BeautifulSoup


def id_from_filename(pathname):
    """ Return the id in the filename of pathname

    :param pathname: string
    :return: string
    """
    return re.search(r"([0-9]+)\.html", pathname).group(1)


def pathnames_from_dir(directory):
    """ Return the list of pathname of files contanied in directory

    :param directory: string
    :return: list of strings
    """
    filenames = list(filter(lambda x: 'html' in x, os.listdir(directory)))
    return list(map(lambda x: directory + x, filenames))


def get_schema(dataset, analyzer):
    """ Return an object Schema with the appropriate structure for the selected dataset

    :param dataset: string
        must be one of ['cranfield', 'time']
    :param analyzer: Whoos analyzer
    :return: Schema object
    """
    if dataset == 'cranfield':
        custom_schema = Schema(id=ID(stored=True), title=TEXT(stored=False, analyzer=analyzer),
                               content=TEXT(stored=False, analyzer=analyzer))
    else:
        custom_schema = Schema(id=ID(stored=True),
                               content=TEXT(stored=False, analyzer=analyzer))

    return custom_schema


if __name__ == "__main__":
    # inputs from command line
    config = build_index_config()
    analyzer_str = config['analyzer']
    dataset_str = config['dataset']

    # index target directory and analyzer
    index_dir = f"{INDEX_PATH}_{dataset_str}_{analyzer_str}"
    analyzer = ANALYZERS[analyzer_str]

    # create index directory
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)
    print(f"Indexing documents to {index_dir}")

    # get schema based on selected dataset
    schema = get_schema(dataset_str, analyzer)

    # create index
    create_in(index_dir, schema)
    ix = index.open_dir(index_dir)
    writer = ix.writer()

    # list of documents to be indexed
    files = pathnames_from_dir(DATASETS[dataset_str]['dir'])

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

    print(f"Indexed {len(files)} documents")
