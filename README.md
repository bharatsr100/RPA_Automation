# Spotify-to-Youtube-Music-Migration

This project automates the process of migrating playlists from Spotify to YouTube Music using Selenium and Python.

## Prerequisites and Installation

1. Python 3.x should be installed on your system.
2. Google Chrome browser should be installed.
3. Selenium and ChromeDriver should be installed. Run the below commands to install them.
   ```bash
   pip install selenium --user
   pip install webdriver-manager --user
   ```


## Script Instructions

1. Make sure you are logged into Spotify and YouTube Music in Chrome Browser.
2. Unpin any pinned tabs and close the Chrome Web Browser.
3. Run the script:
   ```bash
   python fetch_data_and_migrate.py
   ```

## Script Information

1. **fetch_data_and_migrate.py**: This script fetches data from Spotify and migrates it to YouTube Music. It calls `migrate_music.py` internally to migrate the data.
2. **migrate_music.py**: This script is called by `fetch_data_and_migrate.py` to handle the migration of individual playlists. There is no need to execute it separately.

## Usage Examples

To fetch data from Spotify and migrate it to YouTube Music, run:
```bash
python fetch_data_and_migrate.py
```

## Troubleshooting

1. **Issue**: The script cannot find the Chrome browser.
   **Solution**: Ensure that Chrome is installed and the path to ChromeDriver is correctly set up.

2. **Issue**: The script fails to log in to Spotify or YouTube Music.
   **Solution**: Make sure you are logged into both services in Chrome before running the script.

3. **Issue**: The script cannot find certain elements on the page.
   **Solution**: Ensure that the page has fully loaded before the script attempts to interact with it. You may need to increase the sleep time in the script.
4. Additionally logs are being printed in console to keep track of progress and debug if there is any issue.