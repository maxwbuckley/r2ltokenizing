import anthropic
import os
import time

import llmarithmetic

# Set up the client
client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

SYSTEM_PROMPT = "You are a helpful assistant."

total = 0
matches = 0
errors = 0



for i in range(30):
  total += 1

  time.sleep(.01)
  # 3, 3 -> Seems no commas 0.83, commas 0.?
  # 3, 4 -> Seems no commas 0.16, commas 0.6?
  # 4, 6 -> Seems no commas 0.03, commas 0.0?

  PROMPT, expected_answer = llmarithmetic.construct_prompt(3, 4, "-", commas=False)

  response = client.messages.create(
    model="claude-3-5-sonnet-20240620", # "claude-3-haiku-20240307",#"claude-2.1", 
    max_tokens=1000,
    system=SYSTEM_PROMPT,
    messages=PROMPT
  )
  response_text = response.content[0].text
  #response_text = response_text.replace(",","")

  #try:
  #  resp_num = int(response_text)
  #except ValueError:
  #  print("Error got a weird response: '%s'" % response.content[0].text)
  #  resp_num = -1
  #  errors += 1
  if llmarithmetic.compare_responses(response_text, expected_answer):
    matches += 1
    print("%s matched :D" % i)
  #elif llmarithmetic.convert_to_int(expected_answer) == llmarithmetic.convert_to_int(actual_answer)
  else:
    actual_answer = llmarithmetic.extract_last_number(response_text)
    diff = llmarithmetic.convert_to_int(expected_answer) - llmarithmetic.convert_to_int(actual_answer)
    print("Expected: %s, got %s, diff %s" % (expected_answer, actual_answer, diff))
print(matches/total)
print("Errors: %s" % errors)