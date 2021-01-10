from nltk.corpus import wordnet


class wordnet_method:
    def __init__(self):
        pass

    def extend_query(self, query):
        word_arr = []
        for word in query:
            for syn in wordnet.synsets(word):
                for l in syn.lemmas():
                    word_arr.append(l.name())
                    # break
                # break
        word_arr.extend(query)
        set_word = set(word_arr)
        list_word = list(set_word)
        return list_word
