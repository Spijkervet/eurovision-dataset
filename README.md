# Eurovision Song Contest Dataset
[![DOI](https://zenodo.org/badge/214236225.svg)](https://zenodo.org/badge/latestdoi/214236225)

The Eurovision Song Contest is a freely-available dataset containing metadata, contest ranking and voting data of 1562 songs that have competed in the Eurovision Song Contests. The upcoming release will also contain audio features.

Every <b>year</b>, the dataset is updated with the contest's results. This release contains the contestant metadata, contest ranking and voting data of 1562 entries that participated in the Eurovision Song Contest from its first occurrence in 1956 until now. The corresponding audio for every song can be streamed through YouTube.

The metadata and voting data are provided by the [EurovisionWorld](https://eurovisionworld.com) fansite.

### Downloading the dataset
The dataset can be downloaded [here](https://github.com/Spijkervet/eurovision_dataset/releases). To replicate it, follow the instructions at the bottom of the readme.

#### Audio
With the `contestants.csv` in the same folder as the `audio.py` file, the YouTube audio streams of all songs can be collected by running `python3 audio.py`. Alternatively, `sh run.sh audio` or `sh run.sh docker audio` can be used to scrape locally or use a Docker container to scrape the streams.


### Using the dataset in your research paper?
Please contact janne [dot] spijkervet [at] gmail [dot] com


## How to get started
To get an initial idea of the dataset, an example Jupyter Notebook is created in the `examples` directory. This can be opened with `jupyter notebook`. To replacite the dataset, see below or:


### Easy setup
The `run.sh` file makes it easy to either replicate the full dataset or download the latest version and extract the audio features from all the songs. By default, `sh run.sh` will run the scraper from the local Python environment.

Run `sh run.sh docker` to build the Dockerfile and run the `main.py` from within the container. No additional setup should be necessary. This will replicate the dataset, both the `contestants.csv` and `votes.csv` files.

The audio can be scraped from either within or outside the Docker container:
```
sh run.sh docker audio
sh run.sh audio
```


### Audio Features
The audio features can be extracted once all the audio is present in the `audio` folder using:
```
sh audio_features.sh
```
This will launch a Docker container with Essentia's stream music extractor installed. Alternatively, `audio_features.py` can be run given Essentia's extractor is installed in the PATH environment.

## Data description
The competition ranking is provided for both finals and semi-finals. The country-to-country voting data contains 47007 voting activities, and is separated by jury- and televoting after it was introduced in 2016.

### contestants.csv

| column | description |  
|---|---|
| year | contest year |
| to_country_id | country id of contestant | 
| to_country  | country name of contestant |
| performer | artist |
| song | title of the contestant's song |
| sf_num | participated in semi-final 1, 2 or 0 (from 2004-2008 there was only one semi-final) |
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


## Replication
It is recommended to use Docker by running `sh run.sh docker`, or use a local installation by just invoking `sh run.sh`. To also obtain the audio, run either `sh run.sh audio` or `sh run.sh docker audio`.

To replicate the dataset, a WebDriver for either Chrome, Firefox, or Safari is required, e.g. the [WebDriver for Chrome](https://chromedriver.chromium.org/downloads), along with the Selenium Python package (`pip3 install selenium`). Follow the instructions to setup the WebDriver [here](https://chromedriver.chromium.org/getting-started). The project's dependencies can be installed using:
```
pip3 install -r requirements.txt
```

Use the following command to extact the data of all Eurovision Song Contests between 1956 and 2019:
```
python3 main.py --start 1956 --end 2019
```

This will create a `contestants.csv` and `votes.csv` file.

