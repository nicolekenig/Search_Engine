import re

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from document import Document

pattern = re.compile(r"[A-Z][a-z]+|\d+|[A-Z]+(?![a-z])")
# dean
month_dict = {"jan": 'january',
              "feb": 'february',
              'mar': 'march',
              'apr': 'april',
              "jun": 'june',
              "jul": 'july',
              "aug": 'august',
              'sep': 'september',
              "oct": 'october',
              "nov": 'november',
              "dec": 'december'}


class Parse:

    def __init__(self):
        self.stop_words = stopwords.words('english')
        self.stop_words.extend(
            ['', ' ', '=', ',', ":", "//", "/", '.', ';', '}', '{', '``', "''", "/'/", '+', "*", "[", "]", "&", "(",
             ")", '..', '...', '....', '.....', '…', 'RT', 'rt', 'I'])
        self.stop_words_dict = dict.fromkeys(self.stop_words)

    def parse_sentence(self, text):
        """
        This function tokenize, remove stop words and apply lower case for every word within the text
        :param text:
        :return:0
        """
        text_tokens = word_tokenize(text)
        text_tokens_without_stopwords = [w for w in text_tokens if
                                         w.lower() not in self.stop_words_dict and w.isascii()]
        return text_tokens_without_stopwords

    def parse_doc(self, doc_as_list):
        """
        This function takes a tweet document as list and break it into different fields
        :param doc_as_list: list re-preseting the tweet.
        :return: Document object with corresponding fields.
        """

        tweet_id = doc_as_list[0]
        tweet_date = doc_as_list[1]
        full_text = doc_as_list[2]
        url = doc_as_list[3]
        retweet_text = doc_as_list[4]
        retweet_url = doc_as_list[5]
        quote_text = doc_as_list[6]
        quote_url = doc_as_list[7]
        term_dict = {}
        tokenized_text = self.parse_sentence(full_text)
        doc_length = len(tokenized_text)  # after text operations.

        if len(url) > 2:
            url = self.parse_sentence(url)
            tokenized_text.extend(url)

        index = 0
        word = ''
        while index < doc_length - 1:
            try:
                j = 0
                while j < len(tokenized_text[index]) - 1 and (
                        tokenized_text[index][j] == " " or tokenized_text[index][j] == "'" or tokenized_text[index][
                    j] == "=" or tokenized_text[index][j] == "+" or tokenized_text[index][j] == "-" or
                        tokenized_text[index][j] == "." or tokenized_text[index][j] == "," or tokenized_text[index][
                            j] == "_"):
                    j += 1
                tokenized_text[index] = tokenized_text[index][j:]
                word = tokenized_text[index]
                if word != '' and word != " ":
                    if tokenized_text[index] == '#':  # --------- start # ------------
                        if index + 1 < doc_length - 1:
                            word = tokenized_text[index] + tokenized_text[index + 1]
                            word_lower = word.lower()
                            word_lst = ([a.lower() for a in re.split('([A-Z][a-z]+)', word) if a and len(a) > 1])
                            for w in word_lst:  # ***
                                if w in term_dict.keys():
                                    term_dict[w] += 1
                                else:
                                    term_dict[w] = 1

                            if word_lower in term_dict.keys():
                                term_dict[word_lower] += 1
                            else:
                                term_dict[word_lower] = 1
                            index += 1  # --------- end # ------------
                    elif tokenized_text[index] == '@':  # --------- start @ ------------
                        if index + 1 < doc_length - 1:
                            word = tokenized_text[index] + tokenized_text[index + 1]
                            if word in term_dict.keys():
                                term_dict[word] += 1
                            else:
                                term_dict[word] = 1
                            index += 1  # --------- end @ ------------
                    elif tokenized_text[index] == "http" or tokenized_text[
                        index] == "https":  # --------- start URL ------------
                        # if index + 1 < doc_length - 1:
                        word = tokenized_text[index]
                        if word in term_dict.keys():
                            term_dict[word] += 1
                        else:
                            term_dict[word] = 1
                    elif tokenized_text[index][0] == "/":
                        splited_urls = re.split('/|//|  ', tokenized_text[index])
                        for url in splited_urls:
                            if url != '':
                                if url in term_dict.keys():
                                    term_dict[url] += 1
                                else:
                                    term_dict[url] = 1  # --------- end URL ------------
                    # index += 1
                    elif tokenized_text[index][0].isdigit():  # --------- start NUMBERS and % $ ------------
                        word = tokenized_text[index]
                        number = ''
                        i = 0
                        while i < len(tokenized_text[index]):
                            if word[i] != ',':
                                number += word[i]
                            i += 1
                        if number.isnumeric():
                            if int(number) >= 1000:
                                number = self.human_format(int(number))
                                while number[len(number) - 2] == '0':  # O(N)
                                    number = number[:len(number) - 2] + number[len(number) - 1]
                                if number[len(number) - 2] == '.':  # O(N)
                                    number = number[:len(number) - 2] + number[len(number) - 1]
                            elif index + 1 < doc_length - 1:
                                if tokenized_text[index + 1] == 'Thousand' or tokenized_text[
                                    index + 1] == 'thousand':  # O(1)
                                    number = tokenized_text[index] + 'K'
                                    index += 1
                                elif tokenized_text[index + 1] == 'Million' or tokenized_text[
                                    index + 1] == 'million':  # O(1)
                                    number = tokenized_text[index] + 'M'
                                    index += 1
                                elif tokenized_text[index + 1] == 'Billion' or tokenized_text[
                                    index + 1] == 'billion':  # O(1)
                                    number = tokenized_text[index] + 'B'
                                    index += 1
                                elif tokenized_text[index + 1] == '%' or tokenized_text[index + 1] == "percent" or \
                                        tokenized_text[index + 1] == "percentage":
                                    number = tokenized_text[index] + '%'
                                    index += 1
                                elif tokenized_text[index + 1] == '$' or tokenized_text[index + 1] == 'dollar' or \
                                        tokenized_text[index + 1] == 'Dollar' or tokenized_text[index + 1] == 'DOLLAR':
                                    number = tokenized_text[index] + '$'
                                    index += 1
                            if number in term_dict.keys():
                                term_dict[number] += 1
                            else:
                                term_dict[number] = 1  # --------- end NUMBERS and % $ ------------
                    elif tokenized_text[index] in month_dict:  # --------- start month  ------------
                        word = month_dict[tokenized_text[index]]
                        if word in term_dict.keys():
                            term_dict[word] += 1
                        else:
                            term_dict[word] = 1  # --------- end month  ------------
                    else:
                        if len(word) > 1:
                            if word in term_dict.keys():
                                term_dict[word] += 1
                            else:
                                term_dict[word] = 1
            except:
                print('problem in parser')
            index += 1

        document = Document(tweet_id, tweet_date, tokenized_text, url, retweet_text, retweet_url, quote_text, quote_url,
                            term_dict, doc_length)
        return document

    def human_format(self, num):
        magnitude = 0
        while abs(num) >= 1000:
            magnitude += 1
            num /= 1000.0
        # add more suffixes if you need them
        return '%.3f%s' % (num, ['', 'K', 'M', 'B', 'T', 'P'][magnitude])

    #     # split url
    #     if len(url) > 2:
    #         url = url[1: len(url)-1]
    #         url = self.parse_sentence(url)
    #         tokenized_text.extend(url)
    #
    #     #rules
    #     copied_tokenized_text = []
    #     the_index = 0
    #     while the_index < len(tokenized_text):
    #         try:  # new rule: convert word to number
    #             tokenized_text[the_index] = str(w2n.word_to_num(tokenized_text[the_index]))
    #         except:
    #             pass
    #         #chenge number to K M B
    #         if tokenized_text[the_index][0].isdigit() and (',' in tokenized_text[the_index]): #O(N)
    #             tokenized_text[the_index] = tokenized_text[the_index].replace(',', '') #O(N)
    #         if tokenized_text[the_index].isdecimal():
    #             if the_index+1 < len(tokenized_text) - 1: #O(1)
    #                 if tokenized_text[the_index + 1] == 'Thousand' or tokenized_text[the_index + 1] == 'thousand': #O(1)
    #                     str_num = tokenized_text[the_index] + 'K'
    #                     copied_tokenized_text.append(str_num)
    #                     if the_index+2 < len(tokenized_text)-1:
    #                         the_index += 1
    #                 elif tokenized_text[the_index + 1] == 'Million' or tokenized_text[the_index + 1] == 'million':  #O(1)
    #                     str_num = tokenized_text[the_index] + 'M'
    #                     copied_tokenized_text.append(str_num)
    #                     if the_index + 2 < len(tokenized_text) - 1:
    #                         the_index += 1
    #                 elif tokenized_text[the_index + 1] == 'Billion' or tokenized_text[the_index + 1] == 'billion': #O(1)
    #                     str_num = tokenized_text[the_index] + 'B'
    #                     copied_tokenized_text.append(str_num)
    #                     if the_index + 2 < len(tokenized_text) - 1:
    #                         the_index += 1
    #                 elif int(tokenized_text[the_index]) >= 1000:
    #                     num_as_str = self.human_format(int(tokenized_text[the_index]))  #O(N)
    #                     while num_as_str[len(num_as_str) - 2] == '0': #O(N)
    #                         num_as_str = num_as_str[:len(num_as_str) - 2] + num_as_str[len(num_as_str) - 1]
    #                     if num_as_str[len(num_as_str) - 2] == '.':  #O(N)
    #                         num_as_str = num_as_str[:len(num_as_str) - 2] + num_as_str[len(num_as_str) - 1]
    #                     copied_tokenized_text.append(num_as_str)
    #                 else:
    #                     copied_tokenized_text.append(tokenized_text[the_index])
    #         if '#' == tokenized_text[the_index]:
    #             if the_index + 1 < len(tokenized_text)-1:
    #                 word = tokenized_text[the_index] + tokenized_text[the_index+1]
    #                 copied_word = word.lower()
    #                 # copied_word = (copied_word.encode("ascii", "ignore")).decode()
    #                 expanded = [a.lower() for a in re.split('([A-Z][a-z]+)', word) if a and a.isascii()]
    #                 if copied_word not in expanded:
    #                     expanded.append(copied_word)
    #                 if len(expanded) == 1:
    #                     copied_tokenized_text.append(expanded[0][1:])
    #                     copied_tokenized_text.append(copied_word)
    #                 else:
    #                     expanded = expanded[1:]
    #                     copied_tokenized_text.extend(expanded)
    #             the_index += 1
    #
    #         elif 'http' == tokenized_text[the_index] or 'https' == tokenized_text[the_index]:
    #             if the_index + 1 < len(tokenized_text) - 1:
    #                 url_arr = [tokenized_text[the_index], tokenized_text[the_index + 1]]
    #             else:
    #                 url_arr = [tokenized_text[the_index]]
    #             for url in url_arr: #O(N)
    #                 split_url = self.parse_sentence(url) #O(N)
    #                 for to_split in split_url:  #O(N)
    #                     if '/' in to_split:
    #                         to_split = re.split('/|//|  ', to_split)
    #                     if len(to_split) > 0:
    #                         if type(to_split) is str:
    #                             copied_tokenized_text.append(to_split)
    #                         else:
    #                             to_split = list(filter(None, to_split))
    #                             for tokenized_text[the_index] in to_split:
    #                                 copied_tokenized_text.append(tokenized_text[the_index])
    #             the_index += 1
    #         # find and change tags
    #         elif '@' == tokenized_text[the_index]:  #O(1)
    #             if the_index + 1 < len(tokenized_text) - 1:
    #                 tokenized_text[the_index] = tokenized_text[the_index]+tokenized_text[the_index+1]
    #             copied_tokenized_text.append(tokenized_text[the_index])
    #             the_index += 1
    #         # find and change percents
    #         elif 'percentage' == tokenized_text[the_index] or 'percent' == tokenized_text[the_index] or '%' == tokenized_text[the_index]:  #o(n)
    #             if the_index-1 >= 0:
    #                 if tokenized_text[the_index - 1][0].isdigit():
    #                     tokenized_text[the_index - 1] = str(tokenized_text[the_index - 1]) + '%'
    #                 copied_tokenized_text = copied_tokenized_text[0:len(copied_tokenized_text)-1]  #O(n)
    #                 copied_tokenized_text.append(tokenized_text[the_index - 1])
    #         elif '-' in tokenized_text[the_index]:
    #             word_lower = tokenized_text[the_index].lower()
    #             copied_word = word_lower
    #             expanded2 = re.split('-', word_lower)
    #             copied_tokenized_text.append(copied_word)
    #             for i in range(0, len(expanded2)):  # O(n)
    #                 if expanded2[i] == "":
    #                     return []
    #                 else:
    #                     if expanded2[i] == '.' or expanded2[i] == "…" or expanded2[i] == ',' or expanded2[i] == '!' or expanded2[i] == ':' or expanded2[i] == '?' or expanded2[i] == "'" or expanded2[i] == '"':
    #                         expanded2[i] = ''
    #             copied_tokenized_text.extend(expanded2)
    #         # non of the ebov
    #         else:
    #             copied_tokenized_text.append(tokenized_text[the_index])
    #         the_index += 1
    #
    #     term_dict.update(self.add_to_term_dict(term_dict, copied_tokenized_text))
    #     # print(term_dict)
    #     document = Document(tweet_id, tweet_date, tokenized_text, url, retweet_text, retweet_url, quote_text,
    #                         quote_url, term_dict, doc_length)
    #     return document
    #
    # def add_to_term_dict(self, term_dict, split_arr):
    #     for term in split_arr:
    #         if term.isascii() and term != '' and term not in self.stop_words:
    #             if not (term.isalpha() and len(term) <=1 ):
    #                 if ":" in term:
    #                     term = term.replace(':', '')
    #                 if term not in term_dict.keys():
    #                     term_dict[term] = 1  # amount in the doc
    #                 else:
    #                     term_dict[term] += 1
    #     return term_dict
    #
    # def human_format(self, num):
    #     magnitude = 0
    #     while abs(num) >= 1000:
    #         magnitude += 1
    #         num /= 1000.0
    #     # add more suffixes if you need them
    #     return '%.3f%s' % (num, ['', 'K', 'M', 'B', 'T', 'P'][magnitude])
