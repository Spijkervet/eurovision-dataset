
if [ "$1" = "docker" ]; then
    docker build -t python-chromedriver:latest .
    if [ "$2" = "audio" ]; then
        wget -nc https://github.com/Spijkervet/eurovision_dataset/releases/download/1.0/contestants.csv
        docker run -it -w /usr/workspace -v $(pwd):/usr/workspace python-chromedriver:latest python3 audio.py
    else
        docker run -it -w /usr/workspace -v $(pwd):/usr/workspace python-chromedriver:latest python3 main.py
    fi
else
    pip3 install -r requirements.txt
    if [ "$1" = "audio" ]; then
        wget -nc https://github.com/Spijkervet/eurovision_dataset/releases/download/1.0/contestants.csv
        python3 audio.py
    else
        python3 main.py
    fi
fi