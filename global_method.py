import utils


class global_method:

    def __init__(self):
        pass

    def extend_query(self, query):
        matrix = utils.load_obj("global_matrix")
        query1 = []
        for word in query:
            for key, val in matrix.items():
                if key == word:
                    query1.extend([term for term, num in val[1:3]])
        to_return = query.extend(query1)
        return query
