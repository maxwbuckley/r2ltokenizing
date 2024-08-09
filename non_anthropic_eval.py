import deepinfra
from openai import OpenAI
import time


import llmarithmetic

# Create an OpenAI client with your deepinfra token and endpoint
openai = OpenAI(
    api_key="API_KEY"
    # Can use deepinfra if you want nonOpenAI models
    #base_url="https://api.deepinfra.com/v1/openai",
)







# Should this be used in a system message here?
SYSTEM_PROMPT = [{"role": "system", "content": "You are a helpful assistant."}]

total = 0
matches = 0
errors = 0


for i in range(300):
  total += 1

  time.sleep(.01)
  prompt, expected = llmarithmetic.construct_prompt(7, 9, "*", commas=False)


  response = openai.chat.completions.create(
      model="gpt-3.5-turbo", # "gpt-4",# "gpt-4o", #"meta-llama/Meta-Llama-3-70B-Instruct",
      # Anthropic's API passes the system prompt directly.
      messages= SYSTEM_PROMPT + prompt,
      #sys
  )

  response_text = response_content = response.choices[0].message.content  
  if llmarithmetic.compare_responses(response_text, expected):
    matches += 1
    print("%s matched :D" % i)
  else:
    print("%s did not match %s" % (response_text, expected))
    #print("Diff of %s" % (actual - resp_num))
print("Proportion corect = %s" % (matches/total))
print("Errors = %s" % errors)
