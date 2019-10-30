# Eurovision Song Contest Dataset
This repository contains code to create a dataset containing the competition ranking, country-to-country votes, song metadata, lyrics and video/audio data of all the songs that have compated in the Eurovision Song Contests.

## Usage
At this moment, scraping the data only works with the [WebDriver for Chrome](https://chromedriver.chromium.org/downloads), along with the Selenium Python package (`selenium`). Follow the instructions to setup the WebDriver [here](https://chromedriver.chromium.org/getting-started). The project's dependencies can be installed using:
```
pip3 install -r requirements.txt
```

Use the following command to extact the data of all Eurovision Song Contests between 1956 and 2019:
```
python3 main.py --start 1956 --end 2019
```

This will create a `contestants.csv` and `votes.csv` file.

To explore the data, an example `notebook.ipynb` is created. This can be opened with `jupyter notebook`.

## Data description
### contestants.csv

| column | description |  
|---|---|
| year | contest year |
| from_country_id | (country id of contestant | 
| from_country  | country name of contestant |
| performer | artist |
| song | title of the contestant's song |
| sf_num | participated in semi-final 1, 2 or 0 (from 2004-2008 there was only one semi-final |
| running_final | order in the broadcast of the contest's final |
| running_sf | order in the broadcast of the contest's semi-final |
| place_final | place in the final |
| points_final | points in the final |
| place_sf | place in the semi-final |
| points_sf | points in the semi-final |
| points_tele_final | televoting points in the contest's final |
| points_jury_final | juryvoting points in the contest's final |
| points_tele_sf | televoting points in the contest's semi-final |
| points_jury_sf | juryvoting points in the contest's semi-final |
| lyrics | lyrics of the song |
| youtube_url | url to video on YouTube |

### votes.csv
| column | description |  
|---|---|
| year | contest year |
| round | final, semi-final |
| from_country_id | country id of the country giving points |
| to_country_id | country id of the country receiving points |
| from_country | country name of the country giving points |
| to_country | country name of the country receiving points |
| points | number of points given |
