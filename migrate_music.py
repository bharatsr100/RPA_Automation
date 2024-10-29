import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Set up Chrome WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open YouTube Music
driver.get("https://music.youtube.com/")
time.sleep(20)

# Optional: Check if the page title contains "YouTube Music" to confirm the page opened correctly
if "YouTube Music" in driver.title:
    print("YouTube Music page opened successfully!")
else:
    print("Failed to open YouTube Music page.")

# Close the browser after check
driver.quit()
