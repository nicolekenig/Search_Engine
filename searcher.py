
import utils
from global_method import global_method
from ranker import Ranker


# DO NOT MODIFY CLASS NAME
class Searcher:
    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit. The model 
    # parameter allows you to pass in a precomputed model that is already in 
    # memory for the searcher to use such as LSI, LDA, Word2vec models. 
    # MAKE SURE YOU DON'T LOAD A MODEL INTO MEMORY HERE AS THIS IS RUN AT QUERY TIME.
    def __init__(self, parser, indexer, model=None, method=global_method()):
        self._parser = parser
        self._indexer = indexer
        self._ranker = Ranker()
        self._model = model
        self._method = method

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def search(self, query, k=None):
        """ 
        Executes a query over an existing index and returns the number of 
        relevant docs and an ordered list of search results (tweet ids).
        Input:
            query - string.
            k - number of top results to return, default to everything.
        Output:
            A tuple containing the number of relevant search results, and 
            a list of tweet_ids where the first element is the most relavant 
            and the last is the least relevant result.
        """
        query_as_list = self._parser.parse_sentence(query)
        relevant_docs = self._relevant_docs_from_posting(query_as_list)
        # n_relevant = len(relevant_docs)

        ranked_doc_ids = Ranker.rank_relevant_docs(relevant_docs)
        n_relevant = len(ranked_doc_ids)
        return n_relevant, ranked_doc_ids

    # feel free to change the signature and/or implementation of this function 
    # or drop altogether.
    def _relevant_docs_from_posting(self, query_as_list):
        """
        This function loads the posting list and count the amount of relevant documents per term.
        :param query_as_list: parsed query tokens
        :return: dictionary of relevant documents mapping doc_id to document frequency.
        """
        inverted_idx = utils.load_obj("idx_bench")
        inverted_idx = inverted_idx[0]
        relevant_docs = {}
        query_as_list = self._method.extend_query(query_as_list)
        for query_term in query_as_list:
            try:  # an example of checks that you have to do
                if query_term in inverted_idx:
                    data = inverted_idx[query_term][1]  # tuples of (freq,tweet_id)
                    query_term_tuple_list = [query_term_tuple for query_term_tuple in data]  # tweet ids of the term
                    if query_term not in relevant_docs.keys():
                        relevant_docs[query_term] = query_term_tuple_list
                    else:
                        relevant_docs[query_term].extend(query_term_tuple_list)
            except:
                continue
        return relevant_docs


