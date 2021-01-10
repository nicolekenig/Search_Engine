from spellchecker import SpellChecker


class spellChecker_method:

    def __init__(self):
        pass

    def extend_query(self, query):
        spell = SpellChecker()
        new_query = []
        for word in query:
            misspelled = spell.unknown([word])
            if word in misspelled:
                word = spell.correction(word)
            new_query.append(word)

        return new_query
