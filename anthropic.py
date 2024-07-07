import anthropic
import os
import random

# Set up the client
client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

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

for i in range(300):
  total += 1

  time.sleep(.01)
  PROMPT, actual = construct_prompt(17, 19, False)

  response = client.messages.create(
    model="claude-3-haiku-20240307",#"claude-2.1", #"claude-3-5-sonnet-20240620"
    max_tokens=1000,
    system=SYSTEM_PROMPT,
    messages=PROMPT
  )
  response_text = response.content[0].text
  response_text = response_text.replace(",","")

  try:
    resp_num = int(response_text)
  except ValueError:
    print("Error got a weird response: '%s'" % response.content[0].text)
    resp_num = -1
    errors += 1
  if resp_num == actual:
    matches += 1
    print("%s matched :D" % i)
print(matches/total)
print("Errors: %s" % errors)