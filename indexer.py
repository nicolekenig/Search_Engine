import utils
from parser_module import Parse
from stemmer import Stemmer


# DO NOT MODIFY CLASS NAME
class Indexer:
    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def __init__(self, config):
        self.inverted_idx = {}
        self.postingDict = {}
        self.config = config
        self.stemming = "n"
        self.tweet_dict = {}
        self.pars = Parse()
        self.reversed_inverted_index = {}

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def add_new_doc(self, document, documents_list_length=10000):
        """
        This function perform indexing process for a document object.
        Saved information is captures via two dictionaries ('inverted index' and 'posting')
        :param document: a document need to be indexed.
        :return: -
        """

        try:
            document_dictionary = document.term_doc_dictionary
            # self.countDoc += 1
            for term in document_dictionary.keys():
                if self.stemming == 'y':
                    my_stemmer = Stemmer()
                    term = my_stemmer.stem_term(term)
                    # Update inverted index and posting
                if term not in self.inverted_idx.keys():
                    self.inverted_idx[term] = [1, [
                        (document_dictionary[term], document.tweet_id)]]  # amount of doc, freq in the doc, doc id.

                else:
                    self.inverted_idx[term][0] += 1  # amount of doc
                    self.inverted_idx[term][1].append((document_dictionary[term],
                                                       document.tweet_id))  # freq in the doc # doc id

                if term not in self.postingDict.keys():
                    self.postingDict[term] = [(document.tweet_id, document_dictionary[term])]
                else:
                    self.postingDict[term].append((document.tweet_id, document_dictionary[term]))
                # self.countTweet -= 1

                if document.tweet_id not in self.tweet_dict.keys():
                    self.tweet_dict[document.tweet_id] = [[term, document_dictionary[term]], 1,
                                                          0]  # [term,freq in tweet], amount of unique terms in tweet, amount of terms in tweet
                elif document_dictionary[term] > self.tweet_dict[document.tweet_id][0][
                    1]:  # tweet exist, compering between freq in two terms
                    if self.tweet_dict[document.tweet_id][0][
                        1] == 1:  # before change term check if the last term is unique
                        self.tweet_dict[document.tweet_id][
                            1] += 1  # last term is unique: add to the amount of uniqe terms in tweet
                    self.tweet_dict[document.tweet_id][0] = [term,
                                                             document_dictionary[term]]  # change between the terms
                    self.tweet_dict[document.tweet_id][2] += 1
                elif document_dictionary[term] == 1:  # tweet exist, not most common, check if unique
                    self.tweet_dict[document.tweet_id][1] += 1
                    self.tweet_dict[document.tweet_id][2] += 1
        except:
            # print('problem in indexer : add_new_doc')
            # print(traceback.print_exc())
            pass

    def rebuild_inverted_index(self):
        try:
            temp_dict = {}
            for term, val in self.inverted_idx.items():
                is_lower_letter = term.islower()
                word_upper = term.upper()
                word_lower = term.lower()
                amount = int(val[0])
                data = val[1]

                if is_lower_letter and term in temp_dict:  # my word is lower and lower exist in temp dict
                    temp_dict[term][0][0] += amount
                    temp_dict[term][1].extend(data)
                elif is_lower_letter and word_upper in temp_dict:  # my word is lower but upper is in temp dict
                    new_data = temp_dict[word_upper][1] + data
                    temp_dict[term] = [[temp_dict[word_upper][0][0] + amount], new_data]  # replace
                    temp_dict.pop(word_upper)
                elif not is_lower_letter and word_upper in temp_dict:  # my word is upper and upper in temp dict
                    temp_dict[word_upper][0][0] += amount
                    temp_dict[word_upper][1].extend(data)  # append
                elif not is_lower_letter and word_lower in temp_dict:  # my word is upper and lower in temp dict
                    temp_dict[word_lower][0][0] += amount
                    temp_dict[word_lower][1].extend(data)  # append
                elif is_lower_letter:  # my word is lower and not exist in temp dict
                    temp_dict[term] = [[amount], data]  # add
                else:  # my word is upper and not exist in temp dict
                    temp_dict[word_upper] = [[amount], data]  # add

            self.inverted_idx = temp_dict
            for key, data in self.inverted_idx.items():
                self.build_terms_in_tweet_doc(key, data[1])

        except:
            # print(traceback.print_exc())
            pass

    def build_terms_in_tweet_doc(self, term, data):
        try:
            for tuple in data:
                if tuple != None:
                    id = tuple[1]
                    freq = tuple[0]
                    if id in self.reversed_inverted_index:
                        if term not in self.reversed_inverted_index[id]:
                            self.reversed_inverted_index[id].append((term, freq))
                    else:
                        self.reversed_inverted_index[id] = [(term, freq)]
        except:
            # print(traceback.print_exc())
            pass

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def load_index(self, fn):
        """
        Loads a pre-computed index (or indices) so we can answer queries.
        Input:
            fn - file name of pickled index.
        """
        # print('Load ', fn)
        # if fn[len(fn)-4:] == '.pkl':
        #     fn = fn[0:len(fn)-4]
        fn = 'idx_bench'
        inverted_index = utils.load_obj(fn)
        return inverted_index

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def save_index(self, fn):
        """
        Saves a pre-computed index (or indices) so we can save our work.
        Input:
              fn - file name of pickled index.
        """
        utils.save_obj(self.inverted_idx, fn)

    # feel free to change the signature and/or implementation of this function 
    # or drop altogether.
    def _is_term_exist(self, term):
        """
        Checks if a term exist in the dictionary.
        """
        return term in self.postingDict

    # feel free to change the signature and/or implementation of this function 
    # or drop altogether.
    def get_term_posting_list(self, term):
        """
        Return the posting list from the index for a term.
        """
        return self.postingDict[term] if self._is_term_exist(term) else []
