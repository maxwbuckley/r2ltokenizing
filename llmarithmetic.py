import random

# The set of valid operators
OPERATORS = set(["+", "-", "*", "/"])


def format_number(
    number: int, commas: bool = False
) -> str:
  """Adds commas to numbers R2L after every third digit."""
  if commas:
    return format(number, ',')
  else:
    return str(number)

def convert_to_int(number_string: str) -> int:
  """Removes the commas in a number string."""
  number_string = number_string.replace(",", "")
  try:
    return int(number_string)
  except ValueError:
    return -1

def construct_equation(a: int, b: int, operatorn="+", commas: bool = False) -> str:
  """Helper function for constructing the string equations."""
  return "%s %s %s = " % (format_number(a, commas), operatorn, format_number(b, commas))


def create_question_answer_pair(min, max, operator, commas):
  """Creates a random question and correct answer pair.
  
  Args:
    min: The lowest possible random value.
    max: The highest possible random value.
    operation: The mathamatical operator to use.
    commas: Whether to split the numbers right to left with comma seperators.
    
  Returns:
    A tuple of two strings. The equation string and the expected
    answer ("a + b = ", "c")
  
  Raises:
    ValueError: if the operator is not in "+", "-", "*", "/".
    """
  if operator not in OPERATORS:
      raise ValueError("Yikes, you passed an invalid operator, got %s" % operator)
  a = random.randint(min, max)
  b = random.randint(min, max)
  if operator == "-":
    c = a - b
  elif operator == "*":
    c = a * b
  elif operator == "/":
    c = a / b
  else:
    c = a + b
  equation_str = construct_equation(a, b, operator, commas)
  answer_str = format_number(c, commas) 
  return equation_str, answer_str
  
def construct_prompt(digits_lower, digits_upper, operator="+", commas=False, n_shots=8):
  """Constructs a question prompt including optionally few shot examples."""
  messages = []
  min = 10 ** digits_lower
  max = 10 ** (digits_upper + 1) - 1
  for _ in range(n_shots):
    question, answer = create_question_answer_pair(min, max, operator, commas)
    messages.append({"role": "user", "content": question}),
    messages.append({"role": "assistant", "content": answer})
  question, expected_answer = create_question_answer_pair(min, max, operator, commas)
  messages.append({"role": "user", "content": question})
  return messages, expected_answer

import re

# This is a bit too broad as it will match things like 1,,,,,
pattern = r'-?\d[\d,]*'


def extract_last_number(input_string) -> str:
  """Extracts the last number with commas from the model response string."""
  # Use regex to find the last number in the string (may be comma seperated)
  match = re.findall(pattern, input_string)
  #print("Matchie match was: %s" % match)
  if match:
    return match[-1]
  else:
      print("No digits found in %s" % input_string)
      return "-1"  # Return None if no digits are found


def compare_responses(model_response, expected):
  """Compares the response of the model to the expected. This is
     not trivial owing to the magic of LLMs.
  """
  model_answer_guess = convert_to_int(extract_last_number(model_response))
  expected_answer = convert_to_int(expected)
  if model_answer_guess == expected_answer:
    return True
  return False