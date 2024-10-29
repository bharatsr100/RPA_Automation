import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# C:\Users\bhara\AppData\Local\Google\Chrome\User Data

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


# Open YouTube Music
driver.get("https://music.youtube.com/")
time.sleep(30)

# Optional: Check if the page title contains "YouTube Music" to confirm the page opened correctly
if "YouTube Music" in driver.title:
    print("YouTube Music page opened successfully!")
else:
    print("Failed to open YouTube Music page.")

# Close the browser after check
driver.quit()
