if __name__ == '__main__':
    results_file = "output.txt"
    try:

        import sys
        from datetime import datetime

        start = datetime.now()

        import search_engine
        from parser_module import Parse
        from reader import ReadFile

        try:
            from utils import load_inverted_index
        except ImportError:
            with open(results_file, 'w') as f:
                f.write('You are required to implement load_inverted_index() in utils')
                sys.exit(-1)

        test_number = 0
        num_test_failed = 0
        results_summary = []

        reader_inputs = [{'file': 'date=07-08-2020/covid19_07-08.snappy.parquet', 'len': 262794}]

        corpus_path = 'testData'
        output_path = 'posting'
        stemming = False
        queries = ['Banana']
        num_doc_to_retrieve = 10


        def test_part(correct_answers, stud_answers, error_str):
            global test_number, num_test_failed, results_summary
            for correct_answer, stud_answer in zip(correct_answers, stud_answers):
                test_number += 1
                if correct_answer != stud_answer:
                    num_test_failed += 1
                    results_summary.append(f'Test Number: {test_number} Failed to {error_str} '
                                           f'Expected: {correct_answer} but got {stud_answer}')


        def test_reader():
            global num_test_failed, results_summary
            num_test_failed = 0
            r = ReadFile(corpus_path)
            correct_answers = [x['len'] for x in reader_inputs]
            student_answers = [len(r.read_file(x['file'])) for x in reader_inputs]
            test_part(correct_answers, student_answers, error_str="read")
            if num_test_failed == 0:
                results_summary.append('All Reader tests passed')


        def test_run():
            global grade, test_number, num_test_failed
            num_test_failed = 0
            orig_stdout = sys.stdout
            run_file = open('run.txt', 'w')
            sys.stdout = run_file
            try:
                test_number += 1
                search_engine.main(corpus_path, output_path, stemming, queries, num_doc_to_retrieve)
                student_answers_all = [line.rstrip('\n') for line in open('run.txt')]
                student_answers = [len(student_answers_all[i:i + num_doc_to_retrieve]) for i in
                                   range(0, len(student_answers_all), num_doc_to_retrieve)]
                correct_answers = [num_doc_to_retrieve for _ in range(len(queries))]
                test_part(correct_answers, student_answers, error_str="run")
                if num_test_failed == 0:
                    results_summary.append('Running Passed')
                else:
                    results_summary.append('You are printing in your project')
            except Exception as e:
                results_summary.append(
                    f'Test Number: {test_number} Running Main Program Failed with the following error: {e}')
            run_file.close()
            sys.stdout = orig_stdout


        def second_parse_check():
            global test_number, num_test_failed, results_summary
            try:
                inverted_index = load_inverted_index()
            except TypeError:
                try:
                    inverted_index = load_inverted_index(output_path)
                except:
                    with open(results_file, 'w') as f:
                        f.write('You are required to implement load_inverted_index() in utils')
                        sys.exit(-1)
            expected_terms = ['#Asivikelane']
            for term in expected_terms:
                test_number += 1
                try:
                    inverted_index[term]
                except KeyError:
                    num_test_failed += 1
                    results_summary.append(
                        f'Test Number: {test_number} The term {term} was not found in your inverted index')
            if num_test_failed == 0:
                results_summary.append('Second Parser tests passed')


        def check_csv():
            global test_number, results_summary
            test_number += 1
            try:
                with open('results.csv', 'r'):
                    results_summary.append('Results File found')
            except FileNotFoundError:
                results_summary.append('Could Not find file results.csv')


        def check_report():
            global test_number, results_summary
            test_number += 1
            try:
                with open('report.docx', 'r'):
                    results_summary.append('Report File found')
            except FileNotFoundError:
                results_summary.append('Could Not find file report.docx')


        test_reader()
        test_run()
        second_parse_check()
        check_csv()
        check_report()

        run_time = datetime.now() - start
        results_summary.append(f'RunTime was: {run_time}')
        with open(results_file, 'w') as f:
            for item in results_summary:
                f.write(f'{item}\n')
    except Exception as e:
        with open(results_file, 'w') as f:
            f.write(f'Error: {e}')
