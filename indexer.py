import collections
import os
import traceback

from stemmer import Stemmer


class Indexer:

    def __init__(self, config):

        self.inverted_idx = {}
        self.postingDict = {}
        self.config = config
        self.stemming = "n"
        self.countDoc = 0
        self.countTweet = 450000
        self.tweet_dict = {}
        self.reversed_inverted_index = {}

    def add_new_doc(self, document, documents_list_length):
        """
        This function perform indexing process for a document object.
        Saved information is captures via two dictionaries ('inverted index' and 'posting')
        :param document: a document need to be indexed.
        :return: -
        """
        try:
            document_dictionary = document.term_doc_dictionary
            self.countTweet = self.countTweet - 1
            self.countDoc += 1
            # Go over each term in the doc
            for term in document_dictionary.keys():
                if self.stemming == 'y':
                    my_stemmer = Stemmer()
                    term = my_stemmer.stem_term(term)

                if term not in self.postingDict.keys():
                    self.postingDict[term] = [(document.tweet_id, document_dictionary[term])]  # tweet id, freq in tweet
                else:  # in posting dict
                    self.postingDict[term].append(
                        (document.tweet_id, document_dictionary[term]))  # add tweet id, freq in tweet

                if document.tweet_id not in self.tweet_dict.keys():
                    self.tweet_dict[document.tweet_id] = [[term, document_dictionary[term]], 0,
                                                          1]  # [term,freq in tweet], amount of unique terms in tweet, amount of terms in tweet
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

                # after 450000 tweet write terms to text doc
                if self.countTweet == 0 or self.countDoc == documents_list_length:
                    self.postingDict = self.sort_dict(self.postingDict)
                    name = "posting_files/" + 'signs.txt'
                    f = open(name, "a")
                    temp_letter = ''
                    for key in self.postingDict.keys():
                        if key[0].isalpha():
                            if temp_letter != key[0].lower():
                                temp_letter = key[0].lower()
                                name = "posting_files/" + temp_letter + '.txt'
                                f.close()
                                f = open(name, "a")
                        else:
                            name = "posting_files/" + 'signs.txt'
                        f.write(key + ':' + str(self.postingDict[key]) + '\n')

                    f.close()
                    self.postingDict = {}
                    self.countTweet = 450000
                    self.countDoc = 0

        except:
            # print('problem in indexer : add_new_doc')
            print(traceback.print_exc())

    def sort_dict(self, dict):
        return collections.OrderedDict(sorted(dict.items()))

    def build_terms_in_tweet_doc(self, term, values):
        values = self.replace_latters(values)
        values = values.split(')')
        for tuple in values:
            if tuple != '':
                tuple = tuple.split(',')
                if tuple[0] == '':
                    tuple = tuple[1:]
                if len(tuple) == 2:
                    id = tuple[0]
                    freq = tuple[1]
                    if id in self.reversed_inverted_index:
                        if term not in self.reversed_inverted_index[id]:
                            self.reversed_inverted_index[id].append((term, freq))
                    else:
                        self.reversed_inverted_index[id] = [(term, freq)]

    def replace_latters(self, line):
        try:
            copied_line2 = ''
            for i in range(0, len(line)):
                if line[i] != '[' and line[i] != ']' and line[i] != '(' and line[i] != ' ' and line[
                    i] != "'" and line[i] != '\n':
                    copied_line2 += line[i]
            return copied_line2
        except:
            print('problem ranker: replace_latters')

    def read_and_add_to_temp_dict(self, name_doc):
        temp_dict = {}
        f = open(name_doc, 'r')
        line = f.readline()
        line_number = 1
        while line != '\n' and line != '':
            try:
                line = line.split(':')
                if line[0] == '':
                    line = line[1:]
                is_lower_letter = line[0][0].islower()
                word_upper = line[0].upper()
                word_lower = line[0].lower()
                line[1] = line[1][:-1]
                if is_lower_letter and line[0] in temp_dict:  # my word is lower and lower exist in temp dict
                    temp_dict[line[0]] += line[1]  # append
                elif is_lower_letter and word_upper in temp_dict:  # my word is lower but upper is in temp dict
                    temp_dict[line[0]] = temp_dict[word_upper] + line[1]  # replace
                    temp_dict.pop(word_upper)
                elif not is_lower_letter and word_upper in temp_dict:  # my word is upper and upper in temp dict
                    temp_dict[word_upper] += line[1]  # append
                elif not is_lower_letter and word_lower in temp_dict:  # my word is upper and lower in temp dict
                    temp_dict[word_lower] += line[1]  # append
                elif is_lower_letter:  # my word is lower and not exist in temp dict
                    temp_dict[line[0]] = line[1]  # add
                else:  # my word is upper and not exist in temp dict
                    temp_dict[word_upper] = line[1]  # add
                line = f.readline()
            except:
                line = f.readline()
                print('problem indexer: read_and_add_to_temp_dict')

        f.close()
        os.remove(name_doc)
        f = open(name_doc, 'a')
        for key in temp_dict.keys():
            if len(temp_dict[key]) > 25 * 1920:
                f.write(key + ':' + str(temp_dict[key]) + '\n')
                self.inverted_idx[key] = [int(len(line[1]) / 25), line_number]
                line_number += 1
                self.build_terms_in_tweet_doc(key, temp_dict[key])

        f.close()

    # def build_terms_in_tweet_dict (self):
    #     if document.tweet_id not in self.tweet_dict.keys():
    #         self.tweet_dict[document.tweet_id] = [[term, document_dictionary[term]], 0,
    #                                               1]  # [term,freq in tweet], amount of unique terms in tweet, amount of terms in tweet
    #     elif document_dictionary[term] > self.tweet_dict[document.tweet_id][0][
    #         1]:  # tweet exist, compering between freq in two terms
    #         if self.tweet_dict[document.tweet_id][0][1] == 1:  # before change term check if the last term is unique
    #             self.tweet_dict[document.tweet_id][
    #                 1] += 1  # last term is unique: add to the amount of uniqe terms in tweet
    #         self.tweet_dict[document.tweet_id][0] = [term, document_dictionary[term]]  # change between the terms
    #         self.tweet_dict[document.tweet_id][2] += 1
    #     elif document_dictionary[term] == 1:  # tweet exist, not most common, check if unique
    #         self.tweet_dict[document.tweet_id][1] += 1
    #         self.tweet_dict[document.tweet_id][2] += 1
    #
