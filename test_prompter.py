import unittest
import prompter
import testtools

class TestPrompter(unittest.TestCase):
    def test_get_screen(self):
        # Partitions
        #    error
        #        == '' [x] | != '' [x]
        # Coverage
        #     error = ''
        #     error != ''
        text = 'text'
        prompt = 'prompt'

        function = prompter.get_screen
        cases = (
            {'args': [text, prompt, '']},
            {'args': [text, prompt, 'error message']})
        expected_values = (
            'text\n\nprompt > ',
            'text\n\nerror message\n\nprompt > ')

        for results in testtools.run_function_tests(function, cases, expected_values):
            self.assertTrue(*results)

    def test_try_casting(self):
        # Partitions
        #     casting
        #         succeeded [x] | failed [x]
        # Coverage
        #     casting succeeded
        #     casting failed
        function = prompter.try_casting
        cases = (
            {'args': ['1', int, 'no error']},
            {'args': ['s', int, 's isn\'t an int']})
        expected_values = ((1, ''), ('s', 's isn\'t an int'))

        for results in testtools.run_function_tests(function, cases, expected_values):
            self.assertTrue(*results)

    def test_try_meeting_conditions(self):
        # Partitions
        #     conditions length
        #         == 1 [x] | > 1 [x]
        #     'args' length
        #         == 0 [x] | == 1 [x] | > 1 [x]
        #     'kwargs' size
        #         == 0 [x] | == 1 [x] | > 1 [x]
        #     'message'
        #         == '' [x] | != '' [x]
        #     conditions met
        #         == true [x] | == false [x]
        # Coverage
        #     conditions length == 1 | 'args' == 0 | 'kwargs' == 0 |
        #         'message' == '' | conditions not met
        #     conditions length > 1 | 'args' > 1 | 'kwargs' == 1
        #         'message' != ''
        #     'args' == 1 | 'kwargs' > 1 | conditions met
        condition1 = {'function': lambda s: s.isalpha()}
        condition2 = {
            'function': lambda x, a, b, k1='a': x+a in b and k1 not in b,
            'args': ['a', 'aa'], 'kwargs': {'k1': 'b'},
            'message': 'error message'}
        condition3 = {
            'function': lambda x, a, k1=0, k2=1: (x+k1)*k2 == a,
            'args': [6], 'kwargs': {'k1': 3}}

        case1 = {'args': ['123', [condition1]]}
        case2 = {'args': ['b', [condition1, condition2]]}
        case3 = {'args': [3, [condition3]]}

        function = prompter.try_meeting_conditions
        cases = (case1, case2, case3)
        expected_values = ('invalid input', 'error message', '')

        for results in testtools.run_function_tests(function, cases, expected_values):
            self.assertTrue(*results)

if __name__ == '__main__':
    unittest.main()
