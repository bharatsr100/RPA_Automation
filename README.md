# RPA_Automation

## Test Environment Setup

1. Install Python
2. Run the following commands to install Selenium and WebDriver Manager:
   ```bash
   pip install selenium --user
   pip install webdriver-manager --user

## Test Environment Setup

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

1. Make sure chrome is not opened with user date being used in script. Just close the chrome browser.
2. Run the script.
    ```bash
    python migrate_music.py