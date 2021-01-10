from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec


class gloVe_method:

    def __init__(self, glove_input_file='../../../../glove.twitter.27B.25d.txt'):
        self.glove_input_file = glove_input_file
        self.word2vec_output_file = 'glove.twitter.27B.25d.txt.word2vec'

    def extend_query(self, query):
        glove_input_file = 'glove.twitter.27B.25d.txt'
        word2vec_output_file = 'glove.twitter.27B.25d.txt.word2vec'
        glove2word2vec(glove_input_file, word2vec_output_file)
        model = KeyedVectors.load_word2vec_format(self.word2vec_output_file, binary=False)
        result = []
        to_return = query
        for term in query:
            try:
                result.extend([model.most_similar(term)[0], model.most_similar(term)[1], model.most_similar(term)[2]])
            except:
                pass
        for word, val in result:
            to_return.append(word)
        return to_return
