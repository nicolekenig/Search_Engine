import linecache

import utils
from parser_module import Parse
from ranker import Ranker


class Searcher:
    def __init__(self, inverted_index):
        """
        :param inverted_index: dictionary of inverted index
        """
        self.parser = Parse()
        self.ranker = Ranker()
        # self.inverted_index = self.ranker.create_global_method(inverted_index)

    def relevant_docs_from_posting(self, query):
        """
        This function loads the posting list and count the amount of relevant documents per term.
        :param query: query
        :return: dictionary of relevant documents.
        """

        inverted_idx = utils.load_obj("inverted_idx")
        relevant_docs = {}
        query = self.extend_query(query)
        for query_term in query:
            try:  # an example of checks that you have to do
                if query_term[0].isalpha():
                    t = query_term[0].lower()
                    name = "posting_files/" + t + '.txt'
                else:
                    name = "posting_files/" + 'signs.txt'
                line = linecache.getline(name, inverted_idx[query_term][
                    1])  # find the term line number in the relevant posting file
                # if line == '':
                #     break
                line = line.split(":")
                line[1] = self.replace_latters(line[1])
                line[1] = line[1].split(")")
                query_term_tuple_list = [query_term_tuple for query_term_tuple in line[1] if
                                         query_term_tuple != '']  # tweet ids of the term
                # posting_doc = inverted_idx[query_term]
                if query_term not in relevant_docs.keys():
                    relevant_docs[query_term] = query_term_tuple_list
                else:
                    relevant_docs[query_term].extend(query_term_tuple_list)

            except:
                print('term {} not found in posting'.format(query_term))
        return relevant_docs

    def extend_query(self, query):
        matrix = utils.load_obj("matrix")
        # term_position_matrix = utils.load_obj("term_position_matrix")
        # inverted_index = utils.load_obj("inverted_idx")
        query1 = []
        for word in query:
            max_number = 0
            max_term = ''
            for key in matrix.keys():
                if word == key:
                    for val in matrix[key]:
                        if val[1] > max_number and val[0] != word:
                            max_number = val[1]
                            max_term = val[0]
            query1.append(max_term)
            # m = max(matrix[word])
            # i = term_position_matrix.index(m)
            # if i != word:  # check if the max number isn't the original term
            #     query.append(list(inverted_index)[i])
        to_return = query.extend(query1)
        return query

    def replace_latters(self, line):
        copied_line2 = ''
        for i in range(0, len(line)):
            if line[i] != '[' and line[i] != ']' and line[i] != '(' and line[i] != ' ' and line[i] != "'" and line[
                i] != '\n':
                copied_line2 += line[i]
        return copied_line2
