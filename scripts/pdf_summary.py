# This code is written by Kushagra Behere @ Python 3.10 

import pymupdf
import json
import requests as re
import os

Directory_Path = input("Enter directory path where PDF files are present...\n")
api_key = input("\nEnter OpenAI API Key...\n")
prompt_frame = input("\nEnter the the prompt. If want to use the defualt prompt, just press 'Enter' button...\n")
texts = ""
count = 1
file_encoded_texts = []

# Configurations #
temperature = 0
seed = 42
gpt_model = "gpt-4o"
# /Configurations #

# If user does not provide the prompt
if not prompt_frame:
    prompt_frame = """Compare the features of the different items based on their corresponding texts and return the output in tabular format:\n{prompt_texts}.\n Also based on the comparison, suggest which one should be"""

# Listing all PDFs from the input directory
File_Paths = [os.path.join(Directory_Path,f) for f in os.listdir(Directory_Path) if f.endswith(".pdf")]

# Iterating over all PDFs
for file_path in File_Paths:
    try:
        # Open PDF and extract text
        with pymupdf.open(file_path) as pdf_content:
            text = chr(12).join([page.get_text() for page in pdf_content])
            file_encoded_texts.append(f"\ntext {count}: {text}")

        if file_encoded_texts:
             print(f"Text {count} Generated from PDF!")

    except Exception as e:
        print(e)
        
    count += 1

# Concatenating all the PDF texts to a string to be sent in prompt
for txt in file_encoded_texts:
    texts = txt + texts

# Creating prompt with the extracted text
prompt = prompt_frame.format(prompt_texts=texts)

# Sending API request
res = re.post("https://api.openai.com/v1/chat/completions" , headers = {'Authorization' : f'Bearer {api_key}'} , json = {
"model": gpt_model,
"messages": [{"role": "user", "content": prompt}],
"temperature" : temperature,
"seed" : seed 
})

if res.status_code!=200:
        raise Exception("Could not get answer from OpenAI!")

# Converting string response to python dictionary object
res = json.loads(res.text)

# Parsing the API response
difference = res['choices'][0]['message']['content']

print(difference)