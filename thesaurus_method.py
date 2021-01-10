from PyDictionary import PyDictionary


class thesaurus_method:
    def __init__(self):
        pass

    def extend_query(self, query):
        dictionary = PyDictionary()
        word_arr = []
        for word in query:
            try:
                for syn in dictionary.synonym(word):
                    word_arr.append(syn)
            except:
                continue
        word_arr.extend(query)
        set_word = set(word_arr)
        list_word = list(set_word)
        return list_word
