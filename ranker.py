import linecache
import math
import traceback

import utils


class Ranker:
    def __init__(self):
        # self.global_method_arr = []
        self.term_position_matrix = []

    @staticmethod
    def rank_relevant_doc(relevant_doc, k):
        """
        This function provides rank for each relevant document and sorts them by ft-idf algo.
        The current score considers solely the number of terms shared by the tweet (full_text) and query.
        :param relevant_doc: dictionary of documents that contains at least one term from the query.
        :return: sorted list of documents by score
        """
        tweet_dict = utils.load_obj("tweet_dict")
        try:
            final_relevant_doc = {}
            for term in relevant_doc:
                for term_tuple in relevant_doc[term]:
                    term_tuple = term_tuple.split(',')  # tweet_id, freq in tweet
                    if term_tuple[0] == '':
                        term_tuple = term_tuple[1:]
                    fij = int(term_tuple[1])  # i-term, j-tweet
                    if term_tuple[0] in tweet_dict:
                        num_of_terms_in_tweet = tweet_dict[term_tuple[0]][2]
                        idft = len(relevant_doc[term])
                        wij = (fij / num_of_terms_in_tweet) * math.log10(1000000 / idft)  # score
                        if term_tuple[0] not in final_relevant_doc:
                            final_relevant_doc[term_tuple[0]] = wij
                        else:
                            final_relevant_doc[term_tuple[0]] += wij
            return sorted(final_relevant_doc.items(), key=lambda item: int(item[1]), reverse=True)
        except:
            print('problem ranker: rank_relevant_doc')

    @staticmethod
    def retrieve_top_k(sorted_relevant_doc, k=2000):
        """
        return a list of top K tweets based on their ranking from highest to lowest
        :param sorted_relevant_doc: list of all candidates docs.
        :param k: Number of top document to return
        :return: list of relevant document
        """
        return sorted_relevant_doc[:k]

    def create_global_method(self):
        """
        extend query method: global method
        building off-line matrix, and write it to matrix file
        :param  dictionary of inverted index
        """
        # op3: FIX
        """
                extend query method: global method
                building off-line matrix, and write it to matrix file
                :param  dictionary of inverted index
                """
        try:
            inverted_index = utils.load_obj("inverted_idx")
            reversed_inverted_index = utils.load_obj("reversed_inverted_index")
            # f = open('posting_files/matrix.txt', "a")
            term_position_matrix = []
            matrix = {}
            c_dict = {}  # cij
            for term1 in inverted_index:
                if term1[0].isalpha():
                    name = 'posting_files/' + term1[0].lower() + '.txt'
                elif term1[0] == '#':
                    name = "posting_files/#.txt"
                elif term1[0] == '@':
                    name = "posting_files/@.txt"
                else:
                    name = 'posting_files/numbers.txt'

                line = linecache.getline(name, inverted_index[term1][
                    1])  # find the term line number in the relevant posting file
                if line == '':
                    break
                line = line.split(":")
                line[1] = self.replace_latters(line[1])
                term1_tweet_id = line[1].split(")")
                # term1_tweet_id = [tweet_id for tweet_id in line[1] if tweet_id != '']  # tweet ids of the term
                arr = []
                arr_sum = 0

                for t1_tuple in term1_tweet_id:  # tuple = (tweet_id, freq)
                    if len(t1_tuple) > 1:
                        t1_tuple = t1_tuple.split(",")
                        if t1_tuple[0] == '':
                            t1_tuple = t1_tuple[1:]
                        if len(t1_tuple) == 2:
                            term_and_freq = reversed_inverted_index[t1_tuple[0]]
                            # for term2 in inverted_index:
                            #             term2 = ''
                            #             new_term = ''
                            for term_in_tweet in term_and_freq:
                                cii = 0
                                cij = 0
                                cjj = 0
                                sij = 0
                                term2 = term_in_tweet[0]
                                new_term = term1 + term2
                                reversed_new_term = term2 + term1
                                if new_term in c_dict:
                                    continue
                                elif reversed_new_term in c_dict:
                                    cij = c_dict[reversed_new_term]
                                    cii = c_dict[term1 + term1]
                                    cjj = c_dict[term2 + term2]
                                else:
                                    if term2[0].isalpha():
                                        name = 'posting_files/' + term2[0].lower() + '.txt'
                                    elif term2[0] == '#':
                                        name = "posting_files/#.txt"
                                    elif term2[0] == '@':
                                        name = "posting_files/@.txt"
                                    else:
                                        name = 'posting_files/numbers.txt'
                                    line2 = linecache.getline(name, inverted_index[term2][
                                        1])  # find the term line number in the relevant posting file
                                    if line2 == '' or line2 == '\n':
                                        break
                                    line2 = line2.split(":")
                                    # copied_line2 = ''
                                    line2[1] = self.replace_latters(line2[1])
                                    term2_tweet_id = line2[1].split(")")
                                    # term2_tweet_id = [tweet_id for tweet_id in line2[1] if tweet_id != '']  # tweet ids of the term

                                    # for t1_tuple in term1_tweet_id:  # tuple = (tweet_id, freq)
                                    # t1_tuple = t1_tuple.split(',')
                                    # if t1_tuple[0] == '':
                                    #     t1_tuple = t1_tuple[1:]
                                    for t2_tuple in term2_tweet_id:  # tuple = (tweet_id, freq)
                                        if len(t2_tuple) == 2:
                                            t2_tuple = t2_tuple.split(',')
                                            if t2_tuple[0] == '':
                                                t2_tuple = t2_tuple[1:]
                                            if t1_tuple[0] == t2_tuple[0]:  # ids
                                                cij += int(t1_tuple[1]) * int(t2_tuple[1])
                                                # cjj += int(t2_tuple[1])*int(t2_tuple[1])
                                                c_dict[new_term] = cij
                                            cii += int(t1_tuple[1]) * int(t1_tuple[1])
                                            c_dict[term1 + term1] = cii
                                            cjj += int(t2_tuple[1]) * int(t2_tuple[1])
                                            c_dict[term2 + term2] = cjj
                                if new_term in c_dict:
                                    cij = c_dict[new_term]
                                elif reversed_new_term in c_dict:
                                    cij = c_dict[reversed_new_term]
                                cii = c_dict[term1 + term1]
                                cjj = c_dict[term2 + term2]
                                if (cii + cjj - cij) != 0:
                                    sij = cij / (cii + cjj - cij)
                                # else:
                                #     sij = 0
                                if sij > 0:
                                    arr.append([term2, sij])
                                    arr_sum += sij
                if arr_sum > 0:  # threshold line of the term sum to enter the matrix
                    # f.write(str(arr)+'\n')
                    matrix[term1] = arr
                    term_position_matrix.append(term1)
                    # term_position_matrix.append(term1.lower())
            # f.close()
            utils.save_obj(term_position_matrix, "term_position_matrix")
            utils.save_obj(matrix, "matrix")
            # f = open("posting_files/term_position_matrix.txt", 'a')
            # f.write(str(term_position_matrix) + '\n')
            # f.close()
        except:
            print(traceback.print_exc())
            print(t2_tuple, 't2_tuple')
        ##op 1: NOT GOOD
        # print('start matrix')
        # try:
        #     inverted_index = utils.load_obj("inverted_idx")
        #     f = open('posting_files/matrix.txt', "a")
        #     matrix = {}
        #     term_position_matrix = []
        #     for term1 in inverted_index:
        #         if term1[0].isalpha():
        #             name = 'posting_files/' + term1[0].lower() + '.txt'
        #         else:
        #             name = 'posting_files/signs.txt'
        #         line = linecache.getline(name, inverted_index[term1][
        #             1])  # find the term line number in the relevant posting file
        #         if line == '':
        #             break
        #         line = line.split(":")
        #         line[1] = self.replace_latters(line[1])
        #         term1_tweet_id = line[1].split(")")
        #         # term1_tweet_id = [tweet_id for tweet_id in line[1] if tweet_id != '']  # tweet ids of the term
        #         arr = []
        #         arr_sum = 0
        #         for term2 in inverted_index:
        #             if term2[0].isalpha():
        #                 name = 'posting_files/' + term2[0].lower() + '.txt'
        #             else:
        #                 name = 'posting_files/signs.txt'
        #             line2 = linecache.getline(name, inverted_index[term2][
        #                 1])  # find the term line number in the relevant posting file
        #             if line2 == '' or line2 == '\n':
        #                 break
        #             line2 = line2.split(":")
        #
        #             line2[1] = self.replace_latters(line2[1])
        #             term2_tweet_id = line2[1].split(")")
        #             # term2_tweet_id = [tweet_id for tweet_id in line2[1] if tweet_id != '']  # tweet ids of the term
        #             cii = 0
        #             cij = 0
        #             cjj = 0
        #             for t1_tuple in term1_tweet_id:  # tuple = (tweet_id, freq)
        #                 if len(t1_tuple) > 0:
        #                     t1_tuple = t1_tuple.split(',')
        #                     if t1_tuple[0] == '':
        #                         t1_tuple = t1_tuple[1:]
        #                     for t2_tuple in term2_tweet_id:  # tuple = (tweet_id, freq)
        #                         if len(t2_tuple) > 0:
        #                             t2_tuple = t2_tuple.split(',')
        #                             if t2_tuple[0] == '':
        #                                 t2_tuple = t2_tuple[1:]
        #                             if term1 == term2:  # same term
        #                                 cii += int(t1_tuple[1]) * int(t1_tuple[1])
        #                             elif t1_tuple[0] == t2_tuple[0]:  # ids
        #                                 cij += int(t1_tuple[1]) * int(t2_tuple[1])
        #                                 cjj += int(t2_tuple[1]) * int(t2_tuple[1])
        #             if (cii + cjj - cij) != 0:
        #                 sij = cij / (cii + cjj - cij)
        #                 if sij > 0:
        #                     arr.append([term2, sij])
        #                     arr_sum += sij
        #             # else:
        #             #     sij = 0
        #             # arr.append(abs(sij))
        #             # arr.append([term2, sij])
        #             # arr_sum += sij
        #         if arr_sum > 25:  # threshold line of the term sum to enter the matrix
        #             # f.write(str(arr) + '\n')
        #             # term_position_matrix.append(term1.lower())
        #             matrix[term1] = arr
        #             term_position_matrix.append(term1)
        #     f.close()
        #     utils.save_obj(term_position_matrix, "term_position_matrix")
        #     utils.save_obj(matrix, "matrix")
        #     # f = open("posting_files/term_position_matrix.txt", 'a')
        #     # f.write(str(term_position_matrix) + '\n')
        #     # f.close()
        # except:
        #     print(t1_tuple, t2_tuple)

        # op2: CHECK IF GOOD
        # c_dict = {}  # cij
        # inverted_index = utils.load_obj("inverted_idx")
        # reversed_inverted_index = utils.load_obj("reversed_inverted_index")
        # # f = open('matrix.txt', "a")
        # matrix = {}
        # term_position_matrix = []
        # for term1 in inverted_index:
        #     if term1[0].isalpha():
        #         name = "posting_files/" + term1[0].lower() + '.txt'
        #     else:
        #         name = "posting_files/" + 'signs.txt'
        #     line = linecache.getline(name, inverted_index[term1][1])  # find the term line number in the relevant posting file
        #     if line == '':
        #         break
        #     line = line.split(":")
        #     line[1] = self.replace_latters(line[1])
        #     term1_tweet_id = line[1].split(")")
        #     arr = []
        #
        #     for t1_tuple in term1_tweet_id:  # tuple = (tweet_id, freq)
        #         if len(t1_tuple) > 1:
        #             t1_tuple = t1_tuple.split(',')
        #             if t1_tuple[0] == '':
        #                 t1_tuple = t1_tuple[1:]
        #             if len(t1_tuple) > 1:
        #                 try:
        #                     termsAndFreq = reversed_inverted_index[t1_tuple[0]]
        #                 except:
        #                     print(t1_tuple)
        #                 cii = 0
        #                 cij = 0
        #                 cjj = 0
        #                 for term_in_tweet in termsAndFreq:
        #                     term2 = term_in_tweet[0]
        #                     new_term = term1 + term2
        #                     reversed_new_term = term2 + term1
        #                     if reversed_new_term in c_dict:
        #                         cij = c_dict[reversed_new_term]
        #                         cjj = inverted_index[term2][0] ** 2
        #                         cii = inverted_index[term1][0] ** 2
        #                     elif new_term in c_dict:
        #                         cij = c_dict[new_term]
        #                         cjj = inverted_index[term2][0] ** 2
        #                         cii = inverted_index[term1][0] ** 2
        #                     else:
        #                         cii = inverted_index[term1][0] ** 2
        #                         cjj = inverted_index[term2][0] ** 2
        #                         cij = int(t1_tuple[1]) * int(term_in_tweet[1])
        #                         c_dict[new_term] = cij
        #
        #             # for t1_tuple in term1_tweet_id :  # tuple = (tweet_id, freq)
        #             #     if len(t1_tuple)>0:
        #             #         t1_tuple = t1_tuple.split(',')
        #             #         if t1_tuple[0] == '':
        #             #             t1_tuple = t1_tuple[1:]
        #             #         for t2_tuple in term2_tweet_id:  # tuple = (tweet_id, freq)
        #             #             if len(t2_tuple) > 0:
        #             #                 t2_tuple = t2_tuple.split(',')
        #             #                 if t2_tuple[0] == '':
        #             #                     t2_tuple = t2_tuple[1:]
        #             #                 if term1 == term2:  # same term
        #             #                     cii += int(t1_tuple[1]) * int(t1_tuple[1])
        #             #                 elif t1_tuple[0] == t2_tuple[0]:  # ids
        #             #                     cij += int(t1_tuple[1]) * int(t2_tuple[1])
        #             #                     cjj += int(t2_tuple[1]) * int(t2_tuple[1])
        #             # if (cii + cjj - cij) != 0:
        #                     if (cii + cjj - cij) == 0:
        #                         sij = 0
        #                     else:
        #                         sij = cij / (cii + cjj - cij)
        #                     arr.append([term2,sij])
        #     # if sum(arr) > 0:  # threshold line of the term sum to enter the matrix
        #         # f.write(str(arr) + '\n')
        #     matrix[term1] = arr
        #     term_position_matrix.append(term1)
        #
        #
        # # f.close()
        # utils.save_obj(term_position_matrix, "term_position_matrix")
        # utils.save_obj(matrix, "matrix")
        # f = open("term_position_matrix.txt", 'a')
        # f.write(str(term_position_matrix) + '\n')
        # f.close()

    # def term_in_dict(self,term1_tweet_id, term2_tweet_id):
    #     cjj = 0
    #     for t1_tuple in term1_tweet_id:  # tuple = (tweet_id, freq)
    #         if len(t1_tuple) > 0:
    #             t1_tuple = t1_tuple.split(',')
    #             if t1_tuple[0] == '':
    #                 t1_tuple = t1_tuple[1:]
    #         for t2_tuple in term2_tweet_id:  # tuple = (tweet_id, freq)
    #             if len(t2_tuple) > 0:
    #                 t2_tuple = t2_tuple.split(',')
    #                 if t2_tuple[0] == '':
    #                     t2_tuple = t2_tuple[1:]
    #                 if t1_tuple[0] == t2_tuple[0]:  # ids
    #                     cjj += int(t2_tuple[1]) * int(t2_tuple[1])
    #     return cjj
    # def extend_query(self,indexes_arr):
    #     """
    #     find term in the global matrix to add to the query
    #     :param indexes_arr the indexes of the original query terms in the matrix
    #     return terms to add
    #     """
    #     try:
    #         terms = []
    #         inverted_index = utils.load_obj("inverted_idx")
    #         matrix = utils.load_obj("matrix")
    #         for line_number in indexes_arr:
    #             # line = linecache.getline('matrix.txt', line_number+1)  # find the term line number in the relevant posting file
    #             # line = self.replace_latters(line)
    #             # line = line.split(",")
    #             # # print(line)
    #             m = max(line)
    #             i = line.index(m)
    #             if i not in indexes_arr:  # check if the max number isn't the original term
    #                 terms.append(list(inverted_index)[i])
    #         return terms
    #     except:
    #         print('problem ranker: extend_query')

    def replace_latters(self, line):
        try:
            copied_line2 = ''
            for i in range(0, len(line)):
                if line[i] != '[' and line[i] != ']' and line[i] != '(' and line[i] != ' ' and line[i] != "'" and line[
                    i] != '\n':
                    copied_line2 += line[i]
            return copied_line2
        except:
            print('problem ranker: replace_latters')
