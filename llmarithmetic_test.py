import unittest
import random

import llmarithmetic



def test_format_number():
    num = 75632
    str_num = llmarithmetic.format_number(num)
    str_num_with_commas = llmarithmetic.format_number(num, commas=True)
    assert int(str_num) == num
    assert str_num_with_commas == "75,632"

def test_construct_equation():
    num_a = 435789
    num_b = 854331
    equation = llmarithmetic.construct_equation(num_a, num_b, commas=False)
    equation_with_commas = llmarithmetic.construct_equation(num_a, num_b, commas=True)
    equation_with_minus_and_commas = llmarithmetic.construct_equation(num_a, num_b, "-", commas=True)
    equation_with_mult_and_commas = llmarithmetic.construct_equation(num_a, num_b, "*", commas=True)

    assert equation == "435789 + 854331 = "
    assert equation_with_commas == "435,789 + 854,331 = "
    assert equation_with_minus_and_commas == "435,789 - 854,331 = "
    assert equation_with_mult_and_commas == "435,789 * 854,331 = "

def test_construct_prompt():
    random.seed(42)
    
    prompt, solution = llmarithmetic.construct_prompt(2, 5, operator="*", commas=True, n_shots=2)
    expected_prompt = [{'role': 'user', 'content': '670,587 * 116,839 = '},
                       {'role': 'assistant', 'content': '78,350,714,493'},
                       {'role': 'user', 'content': '26,325 * 777,672 = '},
                       {'role': 'assistant', 'content': '20,472,215,400'},
                       {'role': 'user', 'content': '288,489 * 256,887 = '}]
    #print(prompt)
    assert(len(expected_prompt) == 5)
    assert(solution == "74,109,073,743"), "Error got %s" % solution
    assert prompt == expected_prompt, "Error got %s" % prompt
    
def test_convert_to_int():
    assert(7134561, llmarithmetic.convert_to_int("7,134,561"))
    
def test_compare_responses():
    assert llmarithmetic.compare_responses("138,123", "138,123")
    assert not llmarithmetic.compare_responses("138,123", "123")
    assert llmarithmetic.compare_responses("The answer is 138123", "138123")
    assert llmarithmetic.compare_responses("The answer is 138,123", "138,123")
    messy = llmarithmetic.compare_responses("If the question is what is 136,123 + 2000. The answer is 138,123", "138,123")
    assert messy, "Got %s" % messy



test_format_number()
test_construct_equation()
test_construct_prompt()
test_compare_responses()
test_convert_to_int()
print("Great success!")
