# RPA_Automation

## Test Environment Setup

1. Install Python
2. Run the following commands to install Selenium and WebDriver Manager:
   ```bash
   pip install selenium --user
   pip install webdriver-manager --user

## Git Setup

1. Create git repository on github
2. Run the following commands in git cli for initial commit and pushing changes to remote repo:
    ```bash
    git init
    git add .
    git commit -m "Initial Commit. Youtube music page is loading"
    git remote add origin git@github.com:bharatsr100/RPA_Automation.git
    git branch -M main
    git push -u origin main


## Script Instructions

1. Make sure you are logged into Spotify and Youtube Music in Chrome Brwoser. 
2. Upin if there are pinned tabs and Close the Chrome Web Broser.
3. Run the script.
    ```bash
    python fetch_data_and_migrate.py