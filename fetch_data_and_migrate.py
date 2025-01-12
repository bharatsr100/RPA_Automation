"""
This script fetches playlists from Spotify and migrates them to YouTube Music.
It uses Selenium to interact with the web pages and fetches data using Spotify's API.
"""

import time
import os
import requests
import json
import re
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# Configure Chrome to capture network logs
options = webdriver.ChromeOptions()
capabilities = DesiredCapabilities.CHROME
capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--user-data-dir=C:/Users/bhara/AppData/Local/Google/Chrome/User Data")
chrome_options.add_argument("--profile-directory=Default")

# booleans for Spotify Data Fetch and Migration to youtube music
### If you want to fetch data from Spotify and also migrate it to Youtube Music, set both fetch_data and migrate_playlist to True
### If you only want to fetch data from Spotify and not migrate it to Youtube Music, set fetch_data to True and migrate_playlist to False
### If you only want migrate the extracted data to Youtube Music, set fetch_data to False and migrate_playlist to True

fetch_data= False
migrate_playlist = True


if fetch_data:
    # Path to your ChromeDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    try:
        # Open Spotify home page
        driver.get("https://open.spotify.com/")
        time.sleep(10)
        # Wait for the page to load
        driver.implicitly_wait(5)

        # Fetch browser logs
        logs = driver.get_log('performance')

        # Filter network logs for the desired API call
        authorization_token = None
        client_token = None

        for log_entry in logs:
            log_data = log_entry.get('message')
            
            if not log_data:
                continue

            # Parse JSON logs
            try:
                import json
                network_log = json.loads(log_data)
            except json.JSONDecodeError:
                continue

            # Find request headers for the target URL
            if (
                'message' in network_log and
                network_log['message']['method'] == 'Network.requestWillBeSent'
            ):
                request = network_log['message']['params']['request']
                url = request['url']
                # Check if it matches the desired endpoint
                if "https://api-partner.spotify.com/pathfinder/v1/query" in url:
                    headers = request['headers']
                    authorization_token = headers.get('authorization')
                    client_token = headers.get('client-token')
                    break  # Stop once the desired request is found

        # Print the extracted tokens
        if authorization_token and client_token:
            print(f"Authorization Token: {authorization_token}")
            print(f"Client Token: {client_token}")
            print("authorization_token and client_token fetched successfully")
        else:
            print("Could not find the tokens. Make sure the page has fully loaded.")

    finally:
        # Close the browser
        driver.quit()

    # API URL
    fetch_playlist_id_url="https://api-partner.spotify.com/pathfinder/v1/query?operationName=libraryV3&variables=%7B%22filters%22%3A%5B%5D%2C%22order%22%3Anull%2C%22textFilter%22%3A%22%22%2C%22features%22%3A%5B%22LIKED_SONGS%22%2C%22YOUR_EPISODES%22%5D%2C%22limit%22%3A150%2C%22offset%22%3A0%2C%22flatten%22%3Afalse%2C%22expandedFolders%22%3A%5B%5D%2C%22folderUri%22%3Anull%2C%22includeFoldersWhenFlattening%22%3Atrue%2C%22withCuration%22%3Afalse%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%2217d801ba80f3a3d7405966641818c334fe32158f97e9e8b38f1a92f764345df9%22%7D%7D"

    # Headers
    headers = {
        "authorization": authorization_token,
        "client-token": client_token,
        "content-type": "application/json;charset=UTF-8"
    }


    try:
        # Make the API call
        response = requests.get(fetch_playlist_id_url, headers=headers)

        # Check for successful response
        if response.status_code == 200:
            # Parse and store the response body
            response_body = response.json()
            # print(response_body)
            print("API call successful. Response body stored.")
        else:
            print(f"API call failed with status code {response.status_code}: {response.text}")

    except Exception as e:
        print(f"An error occurred: {e}")

   
    response_dict=response_body

    # Initialize an empty list to store the results
    playlist_data = []
    playlist_names= []


    # Navigate through the JSON structure
    for item in response_dict["data"]["me"]["libraryV3"]["items"]:
        data = item["item"]["data"]
        
        # Check if the typename is "Playlist"
        if data.get("__typename") == "Playlist":
            # Extract name and uri
            playlist_name = data.get("name")
            playlist_uri = data.get("uri")
            
            # Store the data in a dictionary
            if(playlist_name and playlist_uri):
                playlist_data.append({"name": playlist_name, "uri": playlist_uri})
                playlist_names.append(playlist_name)

    # Output the result and save the list of playlist in a txt file

    #Storing the playlist names in a seperate file in case I want to handle playlists creation in Youtube Music
    playlist_file=os.path.join(os.getcwd(),"playlist_names.txt")
    with open(playlist_file, "w",encoding="utf-8") as file:
        file.write("\n".join(playlist_names))
    print(f"Playlist Names saved to {playlist_file}")

    print("Extracted Playlists:")
    print("Number of playlists is ",len(playlist_data))
    for playlist in playlist_data:
        print(f"Name: {playlist['name']}, URI: {playlist['uri']}")


    fetch_tracks_url="https://api-partner.spotify.com/pathfinder/v1/query?operationName=fetchPlaylist&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%2273a3b3470804983e4d55d83cd6cc99715019228fd999d51429cc69473a18789d%22%7D%7D"

    outpout_directory=os.path.join(os.getcwd(),"Spotify Playlist","raw_data")
    data_directory=os.path.join(os.getcwd(),"extracted_data")
    os.makedirs(outpout_directory,exist_ok=True)
    os.makedirs(data_directory,exist_ok=True)

    # Function to sanitize playlist name
    def sanitize_filename(playlist_name):
        # Replace invalid characters with an underscore
        return re.sub(r'[^a-zA-Z0-9]', '_', playlist_name)

    for playlist in playlist_data:
        playlist_name = playlist["name"]
        playlist_uri = playlist["uri"]
        safe_playlist_name = sanitize_filename(playlist_name)
        try:
            variables={
                "uri":playlist_uri,
                "offset":0,
                "limit":200
            }
            encoded_variables=json.dumps(variables)

            response=requests.get(
            fetch_tracks_url,
            headers=headers,
            params={"variables":encoded_variables} 
            )

            if response.status_code == 200:

                output_file = os.path.join(outpout_directory,f"{safe_playlist_name}.txt")
                output_data = os.path.join(data_directory,f"{safe_playlist_name}.txt")
                

                names=[]
                names.append(playlist_name)
                json_data = response.json()
                items=json_data["data"]["playlistV2"]["content"]["items"]


                for item in items:
                    name = item["itemV2"]["data"].get("name")
                    if name:
                        names.append(name)
                
            # Write the names to the output file
                with open(output_data, "w",encoding="utf-8") as file:
                    file.write("\n".join(names))
                print(f"Extracted Tracks for playlist '{playlist_name}' saved to {output_data}")

            else:
                print(f"Failed to fetch tracks for playlist '{playlist_name}'. Status: {response.status_code}")


        except Exception as e:
                print(f"Error processing playlist '{playlist_name}':{e}")


# Migrate extracted spotify data to youtube music by processing the extracted data

if migrate_playlist:
    print("Sleeping for 5 seconds before migrating music...")
    time.sleep(5)
    extracted_data_folder = os.path.join(os.getcwd(), "extracted_data")
    for txt_file in os.listdir(extracted_data_folder):
        if txt_file.endswith(".txt"):
            file_path = os.path.join(extracted_data_folder, txt_file)
            with open(file_path, "r", encoding="utf-8") as file:
                # We are storing the playlist name in the first line of the file
                playlist_name = file.readline().strip()
                # Call migrate_music script with file_path and playlist_name
                os.system(f'python migrate_music.py "{file_path}" "{playlist_name}"')

print("Data fetched and migrated successfully")