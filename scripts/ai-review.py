# Jacob Hartt
# Tom Hastings
# CS4300.001
# 03/06/2025

import sys

from openai import OpenAI

if __name__ == "__main__":
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": "Write a haiku about recursion in programming."
            }
        ]
    )

    print(completion.choices[0].message.content)

    # # print all args excluding script name
    # for arg in sys.argv[1:]:
    #     print(arg)

    with open(sys.argv[1], 'r') as diff_file:
      file_content_string = diff_file.read()
      print(file_content_string)

