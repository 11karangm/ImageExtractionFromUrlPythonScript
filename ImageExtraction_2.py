import requests
import os
import logging
import re
import time


url = "https://grandeguerre.icrc.org/api/ArticleApi/GetDocuments/en/778759/720/10001/"
image_base_url = "https://media.grandeguerre.icrc.org/small-resolution/C/G1/"
def get_document_names(url):
    concatenated_strings = []
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        document_urls = []
        documents = data.get("documents", [])
        
        for document in documents:
            document_url = document.get("documentUrl")
            if document_url:
                document_urls.append(image_base_url+document_url)
        
        return document_urls
        
        
    else:
        print("Failed to retrieve page data")
        return None

di=get_document_names(url)
print(di)

output_file_path = 'document_urls.txt'
with open(output_file_path, 'w') as file:
    for document_url in di:
        file.write(document_url + '\n')


