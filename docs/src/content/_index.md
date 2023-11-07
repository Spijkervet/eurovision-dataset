Every <b>year</b>, the dataset is updated with the contest's results. This release contains the audio features, contestant metadata and voting data of 1562 entries that participated in the Eurovision Song Contest from its first occurrence in 1956 until now.

The metadata and voting data are provided by the [EurovisionWorld](https://eurovisionworld.com) fansite.

<div>
<!-- Place this tag where you want the button to render. -->
<a class="github-button" href="https://github.com/spijkervet/eurovision_dataset" data-icon="octicon-star" aria-label="Star ntkme/github-buttons on GitHub">Star</a>

<!-- Place this tag where you want the button to render. -->
<a class="github-button" href="https://github.com/spijkervet/eurovision_dataset/releases" data-icon="octicon-cloud-download" aria-label="Download ntkme/github-buttons on GitHub">Download</a>
</div>

### Using the dataset in your research paper?
Please contact janne [dot] spijkervet [at] gmail [dot] com


<br/>
<br/>
<br/>
<br/>

## How to get started
To get an initial idea of the dataset, an example Jupyter Notebook is created in the `examples` directory. This can be opened with `jupyter notebook`.

## Data description
The competition ranking is provided for both finals and semi-finals. The country-to-country voting data contains 47007 voting activities, and is seperated by jury- and televoting when applicable.

### contestants.csv

column | description
-------|-------|
year | contest year
to_country_id | (country id of contestant
to_country  | country name of contestant
performer | artist
song | title of the contestant's song
sf_num | participated in semi-final 1, 2 or 0 (from 2004-2008 there was only one semi-final
running_final | order in the broadcast of the contest's final
running_sf | order in the broadcast of the contest's semi-final
place_final | place in the final
points_final | points in the final
place_sf | place in the semi-final
points_sf | points in the semi-final
points_tele_final | televoting points in the contest's final
points_jury_final | juryvoting points in the contest's final
points_tele_sf | televoting points in the contest's semi-final
points_jury_sf | juryvoting points in the contest's semi-final
lyrics | lyrics of the song
youtube_url | url to video on YouTube

### votes.csv
column | description
---|---
year | contest year
round | final, semi-final
from_country_id | country id of the country giving points
to_country_id | country id of the country receiving points
from_country | country name of the country giving points
to_country | country name of the country receiving points
points | number of points given


## Replication
To replicate the dataset, a WebDriver for either Chrome, Firefox, or Safari is required, e.g. the [WebDriver for Chrome](https://chromedriver.chromium.org/downloads), along with the Selenium Python package (`selenium`). Follow the instructions to setup the WebDriver [here](https://chromedriver.chromium.org/getting-started). The project's dependencies can be installed using:
```
pip3 install -r requirements.txt
```

Use the following command to extact the data of all Eurovision Song Contests between 1956 and 2019:
```
python3 scrape_votes.py --start 1956 --end 2019
```

This will create a `contestants.csv` and `votes.csv` file.
