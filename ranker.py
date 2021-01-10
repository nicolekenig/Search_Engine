# you can change whatever you want in this module, just make sure it doesn't 
# break the searcher module
import math
from operator import itemgetter

import utils


class Ranker:
    def __init__(self):
        pass

    @staticmethod
    def rank_relevant_docs(relevant_docs, k=None):
        """
        This function provides rank for each relevant document and sorts them by their scores.
        The current score considers solely the number of terms shared by the tweet (full_text) and query.
        :param k: number of most relevant docs to return, default to everything.
        :param relevant_docs: dictionary of documents that contains at least one term from the query.
        :return: sorted list of documents by score
        """
        try:
            tweet_dict = utils.load_obj('idx_bench')
            tweet_dict = tweet_dict[1]
            final_relevant_doc = {}
            for term in relevant_docs:
                for term_tuple in relevant_docs[term]:
                    if len(term_tuple) == 2:
                        fij = int(term_tuple[0])  # freq term i in tweet j
                        tweet_id = term_tuple[1]
                        if tweet_id in tweet_dict:
                            num_of_terms_in_tweet = tweet_dict[tweet_id][2]
                            idft = len(relevant_docs[term])
                            if num_of_terms_in_tweet == 0 or idft == 0:
                                continue
                            wij = (fij / num_of_terms_in_tweet) * math.log10(10000 / idft)  # score
                            if tweet_id not in final_relevant_doc:
                                final_relevant_doc[tweet_id] = wij
                            else:
                                final_relevant_doc[tweet_id] += wij
            relevant = sorted(final_relevant_doc.items(), key=lambda item: int(item[1]), reverse=True)
            to_return = [x[0] for x in relevant]
            return to_return

        except:
            pass

    def create_global_method(self):
        """
        extend query method: global method
        building off-line matrix, and write it to matrix file
        :param  dictionary of inverted index
        """
        try:
            pikl = utils.load_obj('idx_bench')
            inverted_index = pikl[0]
            reversed_inverted_index = pikl[2]
            term_position_matrix = []
            matrix = {}
            c_dict = {}  # cij
            for term1, data1 in inverted_index.items():
                arr = []
                arr_sum = 0

                for freq, tweet_id in data1[1]:  # tuple = (freq,tweet_id)
                    if freq is not None and tweet_id is not None:
                        term_and_freq = reversed_inverted_index[tweet_id]

                        for term2, val in term_and_freq:
                            cii = 0
                            cij = 0
                            cjj = 0
                            sij = 0
                            new_term = term1 + term2
                            reversed_new_term = term2 + term1
                            if new_term in c_dict:
                                continue
                            elif reversed_new_term in c_dict:
                                cij = c_dict[reversed_new_term]
                                cii = c_dict[term1 + term1]
                                cjj = c_dict[term2 + term2]
                            else:
                                term2_tweet_id = inverted_index[term2][1]

                                for freq2, tweet_id2 in term2_tweet_id:  # tuple = (freq,tweet_id)
                                    if freq2 is not None and tweet_id2 is not None:
                                        if tweet_id == tweet_id2:  # ids
                                            cij += int(freq) * int(freq2)
                                            # cjj += int(t2_tuple[1])*int(t2_tuple[1])
                                            c_dict[new_term] = cij
                                        cii += int(freq) * int(freq)
                                        c_dict[term1 + term1] = cii
                                        cjj += int(freq2) * int(freq2)
                                        c_dict[term2 + term2] = cjj

                            if new_term in c_dict:
                                cij = c_dict[new_term]
                            elif reversed_new_term in c_dict:
                                cij = c_dict[reversed_new_term]
                            if term1 + term1 in c_dict and term2 + term2 in c_dict:
                                cii = c_dict[term1 + term1]
                                cjj = c_dict[term2 + term2]
                            if (cii + cjj - cij) != 0:
                                sij = cij / (cii + cjj - cij)
                            if sij > 0:
                                arr.append([term2, sij])
                                arr_sum += sij
                if arr_sum > 0:  # threshold line of the term sum to enter the matrix
                    arr = sorted(arr, key=itemgetter(1), reverse=True)
                    matrix[term1] = arr
                    term_position_matrix.append(term1)

            global_matrix = matrix
            utils.save_obj(global_matrix, 'global_matrix')


        except:
            pass
