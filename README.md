# Bandit - Steal the Show
Tool to gather agency roster lists, find bands available to book in your area, and compare artist popularity statistics

## Scraping 
This project uses lxml web scraping in python to collect the names of artists on agency rosters

## Spotipy
This project uses Spotipy to retrieve artist popularity data to sort and filter artists

## Songkick Search
This project uses the Songkick API to find concerts, tour dates, and availability from bands everywhere.
By searching the concert database, the program finds bands who have an unbooked day before
or after they're scheduled to perform in your metro area. That spare date is the perfect time to snatch them up for
your venue!

## Other Plans
- Functional Web Interface
- Genre classification
- Sorting by popularity, date, or artist name
- Adding Agency to concert search
- Facebook likes of artists
- Google trends

# Setup
1) Install the latest version of Python (https://www.python.org/)
2) In terminal, run 'pip install sys' (you may not have to do this), 'pip install spotipy', 'pip install lxml'
3) Add file config.py with the following lines:
   SPOTIPY_CLIENT_ID      = Spotify API Client_ID
   SPOTIPY_CLIENT_SECRET  = Spotify API Client_Secret
   SPOTIPY_REDIRECT_URI   = Spotify API Redirect_URI
   SONGKICK_API_KEY       = Songkick API Key

4) Copy this repo to your machine or download as a zip and unzip
5) Using Python Idle (installed in step 1), open the 'main.py' file from the downloaded Bandit project and run the module.
6) Bandit should now be running (to the extent that it can).

# Workflows

## Find Available Artists
1. Run main.py
1.5. You may have to give Bandit access to your spotify in a web window and copy-paste the url after done
2. enter 'search'
3. enter the metro area to search (e.g. Boston)
4. enter the earliest date you wish to search in the format YYYY-MM-DD
5. enter the latest date you wish to search in the format YYYY-MM-DD. If you only want to search for one day, just enter the same as previous.

## Get report for agency roster
1. Run main.py
1.5. You may have to give Bandit access to your spotify in a web window and copy-paste the url after done
2. Enter 'report'
3. Enter 'agency' (check AgencyRoster_todo for finished rosters)
4. Enter 'roster' (usually 'full' but currently uta also has a 'usa' one)

## Example Search Output

![](exampleoutput.png?raw=true)

