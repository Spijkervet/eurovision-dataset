# Eurovision Song Contest Dataset
[![DOI](https://zenodo.org/badge/214236225.svg)](https://zenodo.org/badge/latestdoi/214236225)

The Eurovision Song Contest is a freely-available dataset containing metadata, contest ranking and voting data of 1735 songs that have competed in the Eurovision Song Contests. The upcoming release will also contain audio features.

Every <b>year</b>, the dataset is updated with the contest's results. This release contains the contestant metadata, contest ranking and voting data of 1735 entries that participated in the Eurovision Song Contest from its first occurrence in 1956 until now. The corresponding audio for every song can be streamed through YouTube.

The metadata and voting data are provided by the [EurovisionWorld](https://eurovisionworld.com) fansite.

## Downloading the dataset
The dataset can be downloaded [here](https://github.com/Spijkervet/eurovision_dataset/releases). To replicate it, follow the instructions at the bottom of the readme.

## Analysis and extended jury results

John Ashley Burgoyne, Janne Spijkervet, and David John Baker extended this dataset with jury-level data, new audio features, and statistical analyses for [ISMIR 2023](https://ismir2023program.ismir.net/poster_276.html). You can access their data and code at [this repository](https://github.com/Amsterdam-Music-Lab/mirovision).

#### Audio
With the `contestants.csv` in the same folder as the `audio.py` file, the YouTube audio streams of all songs can be collected by running `python3 audio.py`. Alternatively, `sh run.sh audio` or `sh run.sh docker audio` can be used to scrape locally or use a Docker container to scrape the streams.


### Using the dataset in your research paper?
When using these materials please cite the following resources. *I am also interested to hear about projects building on this work, feel free to send an e-mail to: janne [dot] spijkervet [at] gmail [dot] com*

```
@inproceedings{burgoyne_mirovision,
    author       = {John Ashley Burgoyne and Janne Spijkervet and David John Baker},
    title        = {Measuring the {Eurovision Song Contest}: A Living Dataset for Real-World {MIR}},
    booktitle    = {Proceedings of the 24th International Society for Music Information Retrieval Conference},
    year         = 2023,
    address      = {Milan, Italy},
    url          = {https://archives.ismir.net/ismir2023/paper/000097.pdf}
}

@misc{spijkervet_eurovision,
    author       = {Janne Spijkervet},
    title        = {{The Eurovision Dataset}},
    month        = mar,
    year         = 2020,
    doi          = {10.5281/zenodo.4036457},
    version      = {1.0},
    publisher    = {Zenodo},
    url          = {https://zenodo.org/badge/latestdoi/214236225}
}
```


## How to get started
To get an initial idea of the dataset, an example Jupyter Notebook is created in the `examples` directory. This can be opened with `jupyter notebook`. To replicate the dataset, see below:


### Download from source
You can download the entire dataset using the scraping code included in this repository. This will attempt to fetch and process the data from the [EurovisionWorld](https://eurovisionworld.com) website into the csv files that are also made available in the release section of this repository:

- `votes.csv`
- `contestants.csv`
- `betting_offices.csv`

```bash
pip3 install -r requirements.txt

# will yield votes.csv and contestants.csv
python3 scrape_votes.py

# will yield betting_offices.csv
python3 scrape_odds.py
```

Run `sh run.sh docker` to build the Dockerfile and run the `scrape_votes.py` from within the container. No additional setup should be necessary. This will replicate the dataset, both the `contestants.csv`, `votes.csv` and `betting_offices.csv` files.

The audio can be additionally be fetched from either within or outside the Docker container:
```
bash run.sh docker audio
bash run.sh audio
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

Use the following command to extact the data of all Eurovision Song Contests between 1956 and 2023:
```
python3 scrape_votes.py --start 1956 --end 2023
```

This will create a `contestants.csv` and `votes.csv` file.

# Cite
```
@inproceedings{burgoyne_mirovision,
    author       = {John Ashley Burgoyne and Janne Spijkervet and David John Baker},
    title        = {Measuring the {Eurovision Song Contest}: A Living Dataset for Real-World {MIR}},
    booktitle    = {Proceedings of the 24th International Society for Music Information Retrieval Conference},
    year         = 2023,
    address      = {Milan, Italy},
    url          = {https://archives.ismir.net/ismir2023/paper/000097.pdf}
}

@misc{spijkervet_eurovision,
    author       = {Janne Spijkervet},
    title        = {{The Eurovision Dataset}},
    month        = mar,
    year         = 2020,
    doi          = {10.5281/zenodo.4036457},
    version      = {1.0},
    publisher    = {Zenodo},
    url          = {https://zenodo.org/badge/latestdoi/214236225}
}
```
