import requests
import os

def download_file(url, filepath):
    
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    response = requests.get(url)
    
    if response.status_code == 200:
        with open(filepath, "wb") as file:
            file.write(response.content)
        print("File downloaded successfully")
    else:
        print(f"Error downloading file: {response.status_code}")
    
    