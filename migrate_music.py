"""
This script migrates individual playlists from Spotify to YouTube Music.
It uses Selenium to interact with the YouTube Music web page.
"""

import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--user-data-dir=C:/Users/bhara/AppData/Local/Google/Chrome/User Data")
chrome_options.add_argument("--profile-directory=Default")


# Set up Chrome WebDriver
#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Initialize the WebDriver with options
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get("https://music.youtube.com/")
time.sleep(5) 

#Function to close popup if any is open
def close_popup():
    try:
        popup_close_button=driver.find_element(By.XPATH,'//tp-yt-paper-dialog//div[@class="yt-spec-touch-feedback-shape yt-spec-touch-feedback-shape--touch-response"]/div[@class="yt-spec-touch-feedback-shape__fill"]')
        popup_close_button.click()
        print("playlist popup is closed")
    except Exception as e:
        print("no popups are opened")

# Function to search for a single song
def search_song(song_name):
    # Navigate to YouTube Music
    
    # Search for the song
    close_popup()
    search_box = driver.find_element(By.XPATH, '//input[@placeholder="Search songs, albums, artists, podcasts"]')
    search_box.clear()

    try:
        search_box.send_keys(song_name)
        search_box.send_keys(Keys.RETURN)
    except Exception as e:
        print(f"search box issue: {e}")

    time.sleep(2)
    

# Function to add the top result to the playlist
def add_song(count,playlist):
     
    try:
        print(song," to be processed and count is ",count)
        save_button=driver.find_element(By.XPATH,'//div[@class="card-content-container style-scope ytmusic-card-shelf-renderer"]//button[@aria-label="Save to playlist"]')
        save_button.click() #clicks on save to playlist button
        print("Save to playlist button clicked 1")
        time.sleep(2)
        
        visible_popups_script ="""
        const popup = document.querySelector('tp-yt-paper-dialog');
        //console.log(popup.outerHTML);
        //console.log("zIndex--> ",window.getComputedStyle(popup).zIndex);
        if(popup && window.getComputedStyle(popup).display == 'block') {
            return true;
        }

        return false;
        """
        playlist_popup = driver.execute_script(visible_popups_script)

        if playlist_popup:
            print(f"playlist popup list is visible and clicking on {playlist} playlist")
            add_song=driver.find_element(By.XPATH,f'//div[@id="playlists"]//button[@aria-label="{playlist} "]')
            add_song.click() #clicks on the playlist to add songs to playlist
            print(f"clicked on {playlist} playlist successfully")
            

        else:
            print("playlist popup not visible and song is added")

        print(song," added successfully and count is ",count)


    except Exception as e:
        # print(f"Element not found :{e}")
        close_popup()
        try:
            print("element not found inside top result and proceeding to right clicking on the top result")
            song_result=driver.find_element(By.XPATH,'//div[@id="contents"][1]/ytmusic-shelf-renderer[@class="style-scope ytmusic-section-list-renderer"][1]/div[@id="contents" and @class="style-scope ytmusic-shelf-renderer"]/ytmusic-responsive-list-item-renderer[@class="style-scope ytmusic-shelf-renderer"][1]')      
            # Perform a right-click (context click) on the element
            actions = ActionChains(driver)
            actions.context_click(song_result).perform()
            print("Right click performed on the top result")

            save_song=driver.find_element(By.XPATH,'//tp-yt-paper-listbox[@id="items"]/ytmusic-menu-navigation-item-renderer[@class="style-scope ytmusic-menu-popup-renderer"][1]')
            save_song.click()
            print("Save to playlist button clicked 2")
            time.sleep(2)
            
            visible_popups_script2 ="""
            const popup = document.querySelector('tp-yt-paper-dialog');
            //console.log(popup.outerHTML);
            //console.log("zIndex--> ",window.getComputedStyle(popup).zIndex);
            if(popup && window.getComputedStyle(popup).display == 'block') {
                return true;
            }

            return false;
            """
            playlist_popup2 = driver.execute_script(visible_popups_script2)

            if playlist_popup2:
                print(f"playlist popup2 is visible and clicking on {playlist} playlist")
                add_song=driver.find_element(By.XPATH,f'//div[@id="playlists"]//button[@aria-label="{playlist} "]')
                add_song.click() #clicks on the playlist to add songs to playlist
                print(f"clicked on {playlist} playlist successfully 2")

                
            else:
                print("playlist popup not visible and song is added")
                

            print(song," added successfully and count is ",count)
        except NoSuchElementException:

            # Log to skipped_songs.txt if "Save to playlist" button is not found

            print(f"{song} skipped finally - save button not found")
            with open("skipped_songs.txt", "a") as skipped_file:
                skipped_file.write(f"{song} was skipped from {playlist} playlist\n")
        
        

    #add_to_liked.click()  # Click on the option

#file_path = r"C:\Users\bhara\Desktop\Self Projects\RPA_Automation\Spotify Playlist\extracted\Extracted_Hindi Fvr.txt"

# Get file_path and playlist_name from command-line arguments
file_path = sys.argv[1]
playlist_name = sys.argv[2]
print(f"----------------Migrating the Playlist: {playlist_name}---------------")
with open(file_path, "r") as file:
    count = 0
    for i, song in enumerate(file):
        if i == 0:
            continue  # Skip the first line
        count += 1
        song = song.strip()  # Remove any extra whitespace from the song name
        
        # Skip empty lines, if any
        if not song:
            continue

        # Call the function to search for the song
        search_song(song)
        playlist = playlist_name
        # Add the top result to playlist
        add_song(count, playlist)
        time.sleep(2)

print(f"----------------Migration finished for the Playlist: {playlist_name}---------------")
# Quit the driver after completion
driver.quit()