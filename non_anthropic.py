import deepinfra
from openai import OpenAI

# Create an OpenAI client with your deepinfra token and endpoint
openai = OpenAI(
    api_key="API_KEY"
    # Can use deepinfra if you want nonOpenAI models
    #base_url="https://api.deepinfra.com/v1/openai",
)





import os
import random

SYSTEM_PROMPT = "You are a helpful assistant."


total = 0
matches = 0
errors = 0

import time

def format_number(
    number: int, commas: bool = False
):
  if commas:
    return format(number, ',')
  else:
    return str(number)

def construct_prompt(digits_lower, digits_upper, commas=False, n_shots=8):
  messages = []
  min = 10 ** digits_lower
  max = 10 ** (digits_upper+1) - 1
  for i in range(n_shots):
    a = random.randint(min, max)
    b = random.randint(min, max)
    c = a + b
    messages.append({"role": "user", "content": "%s + %s = " % (format_number(a, commas), format_number(b, commas))}),
    messages.append({"role": "assistant", "content": "%s" % (format_number(c, commas))})
  a = random.randint(min, max)
  b = random.randint(min, max)
  actual = a + b
  messages.append({"role": "user", "content": "%s + %s = " % (format_number(a, commas), format_number(b, commas))})
  return messages, actual

import re

pattern = r'(\d+)(?!\d)'


def find_last_integer(input_string):
    # Use regex to find the last integer in the string
    match = re.search(pattern, input_string)
    if match:
        match = match.group().replace(".", "")
        match = match.replace("'", "")
        match = match.replace("\"", "")
        return int(match)  # Convert found digits into an integer
    else:
        print("No digits found in %s" % input_string)
        return -1  # Return None if no digits are found

for i in range(300):
  total += 1

  time.sleep(.01)
  PROMPT, actual = construct_prompt(7, 9, True, n_shots=8)


  response = openai.chat.completions.create(
      model="gpt-3.5-turbo", # "gpt-4",# "gpt-4o", #"meta-llama/Meta-Llama-3-70B-Instruct",
      messages=PROMPT,
  )

  response_text = response_content = response.choices[0].message.content
  response_text = response_text.replace(",","")
  try:
    resp_num = int(response_text)
  except ValueError:
    try:
      pre, post = response_text.split(" = ")
      last_int = find_last_integer(post)
      resp_num = int(last_int)
    except ValueError:
      print("Error regardless, failure :(.")
      print("Tried to repair, got resp %s, wanted %s" %(resp_num, actual))
      resp_num = -1
      errors += 1
  if resp_num == actual:
    matches += 1
    print("%s matched :D" % i)
  else:
    print("%s did not match %s" % (resp_num, actual))
    print("Diff of %s" % (actual - resp_num))
print("Proportion corect = %s" % (matches/total))
print("Errors = %s" % errors)
