# Jacob Hartt
# Tom Hastings
# CS4300.001
# 03/06/2025

import sys
import textwrap

from openai import OpenAI


# Startup open ai client
client = OpenAI()

# Get the diff from command line argument 1
diff = ""
with open(sys.argv[1], 'r') as diff_file:
  diff = diff_file.read()
  # print(diff)

# Provide project context here
project_context = f"""
These code changes are for a django project.  The app is an active interview service
which uses the chatgpt API to create a dynamic interview chat for job-seekers.
""".strip()

# Provide the prompt here
prompt = f"""
At the end of your message, state either FAIL if you found any significant
issues or SUCCESS if the code is acceptable.

{project_context}

Review the following code changes for best practices, security vulnerabilities,
and potential bugs and provide feedback.  Please include a summary section.

```
{diff}
```
""".strip()

# print(prompt)

# Run the prompt
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system", 
            "content": "You are a helpful assistant that provides information in Markdown format."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
)
response = completion.choices[0].message.content

# Print the response
print(response)


# Get last word in the response
raw_result = response.strip().split()[-1] # get last word
plain_result = raw_result.replace("*", "") # remove italics and bold from result

if plain_result == "FAIL":
    sys.exit(1) # FAIL
else:
    sys.exit(0) # SUCCESS



