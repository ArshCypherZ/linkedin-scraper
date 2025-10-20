# LinkedIn Scraper

A Python script using Selenium to scrape job and post search results from LinkedIn.

## Features

* Scrape job listings.
* Scrape posts based on a search query.
* Filter post results to show only those from the **Past 24 hours** and sorted by **Most Recent**.

## Setup

1.  **Install Dependencies:**
    This script requires Python 3 and the following libraries:

    ```bash
    pip install selenium beautifulsoup4
    ```

2.  **Authentication:**
    * Use a browser extension like "Get cookies.txt" to export your cookies from an active LinkedIn session.
    * Save the exported data in a file named `cookies.txt` in the same directory as the script.

## Usage

### Scraping Recent Posts (Scraping Jobs is similar)

The `posts.py` script searches for posts matching a keyword, filtered by "Past 24 hours" and sorted by "Recent".

1.  Open `posts.py` and change the `link` variable to your desired search query URL.
2.  Run the script:
   
    ```bash
    python posts.py
    ```
    The script will print the post author, content, and a link to the actor's profile.
---

### **Disclaimer**

Scraping LinkedIn is against their Terms of Service. This tool is intended for educational purposes only. Use it at your own risk. Your account may be restricted or banned if you misuse this script.
