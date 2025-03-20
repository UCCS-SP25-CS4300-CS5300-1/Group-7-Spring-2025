# Jacob Hartt
# Tom Hastings
# CS4300.001
# 03/06/2025

from datetime import datetime
import sys
import textwrap
from zoneinfo import ZoneInfo

from openai import OpenAI


TIMEZONE = "America/Denver"
TIME_FORMAT = "%m-%d-%Y_%I%M%p"


# Startup open ai client
client = OpenAI()

# Get the diff from command line argument 1
diff = ""
with open(sys.argv[1], 'r') as diff_file:
  diff = diff_file.read()
  # print(diff)
  diff_file.close()

# Provide project context here
project_context = f"""
These code changes are for a web app with a react front end and django back end.
The app is an active interview service which uses the chatgpt API to create a 
dynamic interview chat for job-seekers.
""".strip()

# Provide the prompt here
prompt = f"""
At the end of your message, state either AI_REVIEW_FAIL if you found any significant
issues or AI_REVIEW_SUCCESS if the code is acceptable.

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
    model="o3-mini",
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

# Print the response and write markdown file
print(response)

local_time = datetime.now(ZoneInfo(TIMEZONE)).strftime(TIME_FORMAT)
out_path = f"review-{local_time}.md"

with open(out_path, 'w') as out_file: 
    out_file.write(response)
    out_file.close()

# # Get last word in the response
# raw_result = response.strip().split()[-1] # get last word
# plain_result = raw_result.replace("*", "") # remove italics and bold from result

if "AI_REVIEW_SUCCESS" in response:
    sys.exit(0) # SUCCESS
else:
    sys.exit(1) # FAIL



