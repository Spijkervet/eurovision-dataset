FROM python:3.7

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable ffmpeg

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# set display port
ENV DISPLAY=:99

# upgrade pip
RUN pip install --upgrade pip

# install selenium
RUN pip install selenium==3.141.0 bs4 pandas youtube-dl

# essentia music extractor
RUN wget ftp://ftp.acousticbrainz.org/pub/acousticbrainz/essentia-extractor-v2.1_beta2-linux-x86_64.tar.gz
RUN tar -xvf essentia-extractor-v2.1_beta2-linux-x86_64.tar.gz
RUN mv streaming_extractor_music /bin