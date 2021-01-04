import os
import time

from playsound import playsound

import utils
from configuration import ConfigClass
from indexer import Indexer
from parser_module import Parse
from ranker import Ranker
from reader import ReadFile
from searcher import Searcher


# corpus_path, output_path,
def run_engine(stemming='n'):
    """
    :return:
    """
    number_of_documents = 0

    config = ConfigClass()
    r = ReadFile(corpus_path=config.get__corpusPath())
    p = Parse()
    indexer = Indexer(config)
    indexer.stemming = stemming
    entries = os.listdir('Data')
    start = time.time()
    print(start)
    playsound('Ding.mp3')
    number_of_documents = 0
    i = 1
    # for entire in entries:
    #     documents_list = r.read_file('Data/'+entire)
    #     documents_list_length = len(documents_list)
    # # Iterate over every document in the file
    #     for idx, document in enumerate(documents_list):
    #         parsed_document = p.parse_doc(document)
    #         indexer.add_new_doc(parsed_document, documents_list_length)
    #     # break

    # documents_list = r.read_file(file_name='sample3.parquet')
    # doc_len = len(documents_list)
    # # Iterate over every document in the file
    # for idx, document in enumerate(documents_list):
    #     # parse the document
    #     parsed_document = p.parse_doc(document)
    #     number_of_documents += 1
    #     # index the document data
    #     indexer.add_new_doc(parsed_document, doc_len)

    # utils.save_obj(indexer.postingDict, "posting")
    # indexer.postingDict = None
    # utils.save_obj(indexer.tweet_dict, "tweet_dict")
    # indexer.tweet_dict = None

    # documents = os.listdir('posting_files')
    # for doc in documents:
    #     indexer.read_and_add_to_temp_dict('posting_files/' + doc)
    # # #
    # playsound('Ding.mp3')
    # middle = time.time()
    # print('middle: ',(middle-start)/60," minutes")
    # print('Finished parsing and indexing. Starting to export files')
    #
    # utils.save_obj(indexer.inverted_idx, "inverted_idx")
    # utils.save_obj(indexer.reversed_inverted_index, "reversed_inverted_index")
    # indexer.inverted_idx = None
    # indexer.reversed_inverted_index = None

    r = Ranker()
    # for doc in documents:
    playsound('Ding.mp3')
    r.create_global_method()

    end = time.time()
    print(end)
    print('end: ', (end - start) / 60, " minutes")


def load_index():
    print('Load inverted index')
    inverted_index = utils.load_obj("inverted_idx")
    return inverted_index


def load_tweet_dict():
    print('Load tweet dict')
    tweet_dict = utils.load_obj("tweet_dict")
    return tweet_dict


def search_and_rank_query(query, inverted_index, k, tweet_dict):
    p = Parse()
    to_return = []
    for q in query:
        query_as_list = p.parse_sentence(q)
        searcher = Searcher(inverted_index)
        relevant_docs = searcher.relevant_docs_from_posting(query_as_list)
        ranked_docs = searcher.ranker.rank_relevant_doc(relevant_docs, tweet_dict)
        ans = searcher.ranker.retrieve_top_k(ranked_docs, k)
        to_return.extend(ans)
    return to_return


# corpus_path, output_path, stemming, queries, num_doc_to_retrieve
def main():
    stemming = False
    start_time = time.time()
    if stemming:
        stemming = 'y'
    else:
        stemming = 'n'
        # corpus_path, output_path,

    run_engine(stemming)
    print("Running time: %s seconds" % (time.time() - start_time))
    # dic_list = load_index()
    # tweet_dict = load_tweet_dict()
    # matrix = utils.load_obj("matrix")
    # num_docs_to_retrieve = 10
    playsound('Ding.mp3')
    # search_and_rank_query_dic = search_and_rank_query(queries, dic_list, num_docs_to_retrieve, tweet_dict)
    # print("search_and_rank_query_dic: ", search_and_rank_query_dic)
    # with open('results.csv', 'w', newline='') as csvfile:
    #     for key in search_and_rank_query_dic:
    #             csvfile.write('{} \n'.format(key))
    # stemming = input("do you want to use stemming y/n: ")
    # while stemming != 'y' and stemming != 'n':
    #     stemming = input("do you want to use stemming y/n: ")
    # stemming = 'n'
    # run_engine(stemming)
    # f = open('queries.txt','r')
    #
    # query = f.readline()
    # while query:
    # query = ''
    # query = input("Please enter a query: ")
    # k = int(input("Please enter number of docs to retrieve: "))
    # k=5
    # inverted_index = load_index()
    # matrix = utils.load_obj("matrix")

    # tweet_dict = load_tweet_dict()
    # for doc_tuple in search_and_rank_query(query, inverted_index, k, tweet_dict):
    #     print('tweet id: {}, score (unique common words with query): {}'.format(doc_tuple[0], doc_tuple[1]))
    # query = f.readline()
