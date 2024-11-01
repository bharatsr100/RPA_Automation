import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# User Data path --> C:\Users\bhara\AppData\Local\Google\Chrome\User Data

# Setup Chrome options
chrome_options = Options()
#chrome_options.add_argument('--headless')
#chrome_options.add_argument("--no-sandbox")
#chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--user-data-dir=C:/Users/bhara/AppData/Local/Google/Chrome/User Data")
chrome_options.add_argument("--profile-directory=Default")



# Set up Chrome WebDriver
#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Initialize the WebDriver with options
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get("https://music.youtube.com/")
time.sleep(5) 

# Function to search for a single song
def search_song(song_name):
    # Navigate to YouTube Music
    
    # Search for the song
    search_box = driver.find_element(By.XPATH, '//input[@placeholder="Search songs, albums, artists, podcasts"]')
    search_box.clear()
    outer_html = search_box.get_attribute('outerHTML')
    print(outer_html)
    search_box.send_keys(song_name)
    search_box.send_keys(Keys.RETURN)
    time.sleep(5)
    

# Function to add the top result to the playlist
def add_song(count):

    save_button=driver.find_element(By.XPATH,'//div[@class="card-content-container style-scope ytmusic-card-shelf-renderer"]//button[@aria-label="Save to playlist"]')
    save_button.click() #clicks on save to playlist button
    

    if count == 1:
        time.sleep(5)
        add_song=driver.find_element(By.XPATH,'//div[@id="playlists"]//button[@aria-label="Spotify Liked "]')
        add_song.click() #clicks on the playlist to add songs to playlist

    
    #add_to_liked.click()  # Click on the option

file_path = r"C:\Users\bhara\Desktop\Self Projects\RPA_Automation\Spotify Playlist\Liked_Filtered_v1.txt"
with open(file_path, "r") as file:
    count=0
    for song in file:
        count += 1
        song = song.strip()  # Remove any extra whitespace from the song name
        
        # Skip empty lines, if any
        if not song:
            continue

        # Call the function to search for the song
        search_song(song)
        
        # Add the top result to liked songs
        add_song(count)
        print(song," added successfully and count is ",count)
        # Optional: Wait a little to avoid overwhelming the system
        time.sleep(2)


# Quit the driver after completion (optional, can keep it open for further actions)
# driver.quit()