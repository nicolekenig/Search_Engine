# df = pd.DataFrame(
#     {'query': [1, 1, 2, 2, 3], 'Tweet_id': [12345, 12346, 12347, 12348, 12349], 'label': [1, 0, 1, 1, 0]})
#
# test_number = 0
# results = []

# precision(df, True, 1) == 0.5
# precision(df, False, None) == 0.5
def precision(df, single=False, query_number=None):
    """
        This function will calculate the precision of a given query or of the entire DataFrame
        :param df: DataFrame: Contains tweet ids, their scores, ranks and relevance
        :param single: Boolean: True/False that tell if the function will run on a single query or the entire df
        :param query_number: Integer/None that tell on what query_number to evaluate precision or None for the entire DataFrame
        :return: Double - The precision
    """
    # the function will run on the entire df
    if len(df['query']) == 0 or df is None:
        return 0
    arr = []
    if not single:
        for query_num in range(1, max(df['query'])):
            temp_df = (df.loc[df['query'] == query_num])
            temp_df = temp_df.reset_index(drop=True)
            num_of_relevant_docs = 0
            for i in range(0, len(temp_df)):
                if temp_df['label'][i] == 1:
                    num_of_relevant_docs += 1
            arr.append(num_of_relevant_docs / len(temp_df))
        if max(df['query']) == 0:
            return 0
        else:
            return sum(arr) / max(df['query'])
    else:
        total_number_of_docs_retrieved = 0
        num_of_relevant_docs_retrieved = 0
        for i in range(0, len(df['query'])):
            if df['query'][i] == query_number:
                total_number_of_docs_retrieved += 1
                if df['label'][i] == 1:
                    num_of_relevant_docs_retrieved += 1
        if total_number_of_docs_retrieved == 0:
            return 0
        else:
            return num_of_relevant_docs_retrieved / total_number_of_docs_retrieved


# recall(df, {1:2}, True) == 0.5
# recall(df, {1:2, 2:2, 3:1}, False) == 0.388
def recall(df, num_of_relevant):
    """
        This function will calculate the recall of a specific query or of the entire DataFrame
        :param df: DataFrame: Contains query numbers, tweet ids, and label
        :param num_of_relevant: Dictionary: number of relevant tweets for each query number. keys are the query number and values are the number of relevant.
        :return: Double - The recall
    """
    my_dict = {}
    if len(df['query']) == 0 or df is None:
        return 0
    num_of_relevant_docs_retrieved = 0
    for i, row in df.iterrows():
        if row['label'] == 1:
            if row['query'] in my_dict.keys():
                my_dict[row['query']] += 1
            else:
                my_dict[row['query']] = 1
    for key in num_of_relevant:
        if key in my_dict.keys():
            if num_of_relevant[key] != 0:
                num_of_relevant_docs_retrieved += my_dict[key] / num_of_relevant[key]
            else:
                return None
    if len(num_of_relevant.keys()) != 0:
        return num_of_relevant_docs_retrieved / len(num_of_relevant.keys())
    return None


def precision_at_n(df, query_number=1, n=5):
    """
        This function will calculate the precision of the first n files in a given query.
        :param df: DataFrame: Contains tweet ids, their scores, ranks and relevance
        :param query_number: Integer/None that tell on what query_number to evaluate precision or None for the entire DataFrame
        :param n: Total document to splice from the df
        :return: Double: The precision of those n documents
    """
    if len(df['query']) == 0 or df is None:
        return 0
    counter = 0
    arr = []
    if query_number is None:
        for query_num in range(1, max(df['query'])):
            if counter == n:
                break
            temp_df = (df.loc[df['query'] == query_num])
            temp_df = temp_df.reset_index(drop=True)
            num_of_relevant_docs = 0
            for i in range(0, len(temp_df)):
                if temp_df['label'][i] == 1:
                    num_of_relevant_docs += 1
                counter += 1
            arr.append(num_of_relevant_docs / len(temp_df))
            if n == 0:
                return 0
            else:
                return sum(arr) / n
    else:
        total_number_of_docs_retrieved = n
        num_of_relevant_docs_retrieved = 0
        for i in range(0, len(df['query'])):
            if counter == n:
                break
            if df['query'][i] == query_number and df['label'][i] == 1:
                num_of_relevant_docs_retrieved += 1
            counter += 1
        if total_number_of_docs_retrieved == 0:
            return 0
        else:
            return num_of_relevant_docs_retrieved / total_number_of_docs_retrieved


# map(df) == 2/3
def map(df):
    """
        This function will calculate the mean precision of all the df.
        :param df: DataFrame: Contains tweet ids, their scores, ranks and relevance
        :return: Double: the average precision of the df
    """
    if len(df['query']) == 0 or df is None:
        return 0
    query_dict = {}
    for query_num in range(1, max(df['query'])):
        temp_df = (df.loc[df['query'] == query_num])
        temp_df = temp_df.reset_index(drop=True)
        for i in range(0, len(temp_df)):
            if temp_df['label'][i] == 1:
                result = precision_at_n(temp_df, query_num, i + 1)
                if query_num not in query_dict:
                    query_dict[query_num] = [result]
                else:
                    query_dict[query_num].append(result)
    queries_avg = []
    for query in query_dict.keys():
        queries_avg.append(sum(query_dict[query]) / len(query_dict[query]))
    if max(df['query']) == 0:
        return 0
    else:
        return sum(queries_avg) / max(df['query'])

#
# def test_value(func, expected, variables):
#     """
#         This function is used to test your code. Do Not change it!!
#         :param func: Function: The function to test
#         :param expected: Float: The expected value from the function
#         :param variables: List: a list of variables for the function
#     """
#     global test_number, results
#     test_number += 1
#     result = func(*variables)  # Run functions with the variables
#     try:
#         result = float(f'{result:.3f}')
#         if abs(result - float(f'{expected:.3f}')) <= 0.01:
#             results.extend([f'Test: {test_number} passed'])
#         else:
#             results.extend([f'Test: {test_number} Failed running: {func.__name__}'
#                             f' expected: {expected} but got {result}'])
#     except ValueError:
#         results.extend([f'Test: {test_number} Failed running: {func.__name__}'
#                         f' value return is not a number'])

#
# if __name__ == '__main__':
#     test_value(precision, 0.5, [df, True, 1])
#     test_value(precision, 0.5, [df, False, None])
#     test_value(recall, 0.5, [df, {1: 2}])
#     test_value(recall, 0.388, [df, {1: 2, 2: 3, 3: 1}])
#     test_value(precision_at_n, 0.5, [df, 1, 2])
#     test_value(precision_at_n, 0, [df, 3, 1])
#     test_value(map, 2 / 3, [df])
#     for res in results:
#         print(res)
