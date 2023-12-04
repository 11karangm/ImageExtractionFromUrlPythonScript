import requests
import os
import logging
import re
import time


log_filename = "download_log.txt"
logging.basicConfig(filename=log_filename, level=logging.ERROR, format="%(asctime)s - %(levelname)s: %(message)s")



important_id = "224"
page_name_url = "https://grandeguerre.icrc.org/api/FileMarkerApi/GetPages/"+important_id
# page_name_url = 'https://grandeguerre.icrc.org/en/File/Search/#/6/2/246/0/French%20or%20Belgian/Military/'
base_url = "https://grandeguerre.icrc.org/api/FileMarkerApi/GetFileStacks/en/"+important_id+"/"
folder_base_url = "https://grandeguerre.icrc.org/api/FileApi/GetFilestacksForFileMarker/en/"
image_base_url = "https://media.grandeguerre.icrc.org/small-resolution/C/G1/"

page_names = []

def get_page_names(url):
    concatenated_strings = []
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for page in data["pages"]:
            start_with = page["startsWith"]
            end_with = page["endsWith"]
            concatenated_string = f"{start_with} ~ {end_with}"
            concatenated_strings.append(concatenated_string)
        return concatenated_strings  # Add this line to return the list
    else:
        print("Failed to retrieve page data")
        return None


# Function to fetch data for a specific ID
def fetch_data_for_id(id):
    url = folder_base_url + str(id)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Failed to retrieve data for ID:", id)
        return None

# Function to download and save images with exception handling
def download_and_save_image(image_url, image_path):
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(image_path, 'wb') as file:
                file.write(response.content)
                # Write the image URLs to the text file
                text_file.write(f"{image_url} = {image_path}\n")
                print(f"Downloaded image: {image_url}")
        else:
            logging.error(f"Failed to download image: {image_url}")
    except Exception as e:
        logging.error(f"Exception while downloading image: {image_url}, Error: {str(e)}")
        

page_names = get_page_names(page_name_url)
if page_names is None:
    # Initialize the list if it's None
    page_names = []

    # Add an element to the list
    page_names.append("Default")
length = len(page_names)
start=0
end=20
quotient= length//20
lengthloop=quotient+1
# for section in range (lengthloop):
# Iterate through paths 0 to 5
#CHANGE THIS COUNT VARIABLE WHEN RERUN AFTER ERROR, KEEP AS ZERO IF RUNNING FOR FIRST TIME.
try:
    count=0
    for path in range(count,length):  # Loop from 0 to 5
        print(str(count)+"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        count=count+1
        json_url = f"{base_url}{path}/"

        # Send an HTTP GET request to the URL
        
        response = requests.get(json_url)
            
        parent_folder = str(page_names[path])
        if not os.path.exists(parent_folder):
            os.mkdir(parent_folder)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
                
                # Extract 'id' values from the 'records' array
                #ids = [record["id"] for record in data["records"]]
                    
                #values = [record["groups"][0]["values"][0]["fileMarkerCaption"]["values"][0]["value"] for record in data["records"]]
                #fileMarkerCaption = data["groups"][0]["values"][0]["fileMarkerCaption"]["values"][0]["value"]
                    
            for record in data["records"]:
                count =0
                data = fetch_data_for_id(record["id"])
                out=''
                input_string = str(record["groups"][0]["values"][0]["fileMarkerCaption"]["values"][0]["value"])
                # Extract the first and last words from each part
                # Split the string by "~" to separate the parts
                parts = input_string.split(" ")
                if len(parts) >= 2:
                    first_part = parts[0]  # Extract the last word from the first part
                    last_part = parts[-1]  # Extract the first word from the last part
                    out=first_part+last_part
                    # print("First Word:", first_part)
                    # print("Last Word:", last_part)
                else:
                    print("Not enough parts found.")

                file_paths_and_names = [f"{entry['files'][0]['filePath']}/{entry['files'][0]['fileName']}" for entry in data]
                        
                text_file_path =input_string+'.txt'
                pattern = r'[\/\\:*?"<>|]'
                cleaned_text_file_name = re.sub(pattern, '', text_file_path)
                text_file = open(cleaned_text_file_name, "w")
                            
                # Create a folder if it doesn't exist
                #if not os.path.exists(sub_folder_name):
                #    os.mkdir(sub_folder_name)
                        
                for file_path_and_name in file_paths_and_names:
                    # Construct image URLs
                    image_url = image_base_url + file_path_and_name
                    image_url_0 = image_url + "_0.JPG"
                    image_url_1 = image_url + "_1.JPG"
                            
                        
                    text_file.write(f"{image_url_0}\n")
                    text_file.write(f"{image_url_1}\n")
                    # print(f"Image URL: {image_url_0}")
                    # print(f"Image URL: {image_url_1}")
                            
                # Close the text file
                text_file.close()   
                count=count+1
                if(count==5):
                    break             
        else:
            print("Failed to retrieve data. Status code:", response.status_code)
    # Pause for 10 minutes
    
finally:
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("++++++++++++++++++++++++++++++++++++++PUT COUNT AS "+str(count)+"WHEN ERROR AND RERUN++++++++++++++++++++++++++++++++++++++")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("Pausing for 10 minutes...")

    # if end+1 < length:
    #     start=end+1
        
    # if start+20 <= length:
    #     end=start+20
    # else:
    #     end = length - start
    

