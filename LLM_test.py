# import library "os"
import os
# import Function "load_dotenv" from "dotenv" library
from dotenv import load_dotenv
# import Function "openAI" from "openai" library
from openai import OpenAI

# Load the API from the file ".env"
load_dotenv()
HF_Token=os.getenv("HF_TOKEN")

# Connect the LLM ( Link Provide us in the APIs.txt file )
client=OpenAI(base_url="https://router.huggingface.co/v1",api_key=HF_Token)

# This provide response from the openai (LLM) , model link in "APIs.txt" file
response=client.chat.completions.create(model="openai/gpt-oss-120b",
                               messages=[{
                                   "role":"user",
                                   "content":"What is good source of protein in Vegetarain",
                               }])
# This provide the answer
answer=response.choices[0].message.content
print(answer)