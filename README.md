# Song Sentiment Analysis


## About The Project

This project uses the Vader module of the Natural Learning Toolkit to conduct sentiment analysis on the lyrics of different Fall Out Boy albums over time. While this project focuses on Fall Out Boy, the functions would work on any other band or artist whose lyrics are on [AZ Lyrics](https://www.azlyrics.com/) where this project sources lyrics from. This is the second project in Olin's [Software Design](https://softdes.olin.edu) course.

### Built With
This project was built using the following libraries:

* [Requests Library](https://requests.readthedocs.io/en/master/)
* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [Natural Language Toolkit](https://www.nltk.org/index.html)


<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these steps.

1. Clone the repo
```sh
git clone https://github.com/MayaSimone/song_sentiment_analysis.git
```
2. [Install](https://requests.readthedocs.io/en/master/user/install/) the Requests library
```sh
$ python -m pip install requests
```
3. [Install](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup) the Beautiful Soup library
```sh
$ apt-get install python3-bs4
```
4. [Install](https://www.nltk.org/install.html) the Natural Learning Toolkit
```sh
$ pip install --user -U nltk
```
*Note the Natural Learning toolkit will also require you to run the following code in a Python interpretter in order to use the Vader Module.
```python
nltk.downloader.download('vader_lexicon')
```

<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements


Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for
Sentiment Analysis of Social Media Text. Eighth International Conference on
Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.
