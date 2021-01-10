import pandas as pd

import utils
from indexer import Indexer
from parser_module import Parse
from searcher import Searcher
# DO NOT CHANGE THE CLASS NAME
from spellChecker_method import spellChecker_method


class SearchEngine:
    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation, but you must have a parser and an indexer.
    def __init__(self, config=None):
        self._config = config
        self._parser = Parse()
        self._indexer = Indexer(config)
        self._model = None
        self._method = spellChecker_method()

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def build_index_from_parquet(self, fn):
        """
        Reads parquet file and passes it to the parser, then indexer.
        Input:
            fn - path to parquet file
        Output:
            No output, just modifies the internal _indexer object.
        """
        df = pd.read_parquet(fn, engine="pyarrow")
        documents_list = df.values.tolist()
        # Iterate over every document in the file
        number_of_documents = 0
        doc_len = len(documents_list)
        for idx, document in enumerate(documents_list):
            # parse the document
            parsed_document = self._parser.parse_doc(document)
            number_of_documents += 1
            # index the document data
            self._indexer.add_new_doc(parsed_document, doc_len)
        # print('Finished parsing and indexing.')

        # print('Finished marge, start rebuild posting dict')
        # self._indexer.rebuild_postingDict()
        self._indexer.rebuild_inverted_index()
        # print('finished rebuild inverted index')

        to_save = (self._indexer.inverted_idx, self._indexer.tweet_dict, self._indexer.reversed_inverted_index)
        utils.save_obj(to_save, 'idx_bench')
        # TODO: inverted_idx, tweet_dict,reversed_inverted_index, to_save change to None
        self._indexer.inverted_idx = None
        self._indexer.tweet_dict = None
        self._indexer.reversed_inverted_index = None
        to_save = None
        # print('Finished rebuild inverted index and build reversed_inverted_index')

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def load_index(self, fn):
        """
        Loads a pre-computed index (or indices) so we can answer queries.
        Input:
            fn - file name of pickled index.
        """

        self._indexer.load_index(fn)

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def load_precomputed_model(self, model_dir=None):
        """
        Loads a pre-computed model (or models) so we can answer queries.
        This is where you would load models like word2vec, LSI, LDA, etc. and 
        assign to self._model, which is passed on to the searcher at query time.
        """
        pass

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def search(self, query):
        """ 
        Executes a query over an existing index and returns the number of 
        relevant docs and an ordered list of search results.
        Input:
            query - string.
        Output:
            A tuple containing the number of relevant search results, and 
            a list of tweet_ids where the first element is the most relavant 
            and the last is the least relevant result.
        """
        searcher = Searcher(self._parser, self._indexer, model=self._model, method=self._method)
        return searcher.search(query)
