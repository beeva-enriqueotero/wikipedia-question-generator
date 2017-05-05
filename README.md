wikipedia-question-generator
============================

Uses Natural Language Processing and Wikipedia content to try to generate Mad Libs-style game questions.

Built for [TrackMaven Monthly Challenge meetup](http://www.meetup.com/TrackMaven-Monthly-Challenge/events/218683569/) in December 2014.

I also made [a short presentation](http://slides.com/atbaker/trackmaven-monthly-challenge-demo) about the project. See [this YouTube video](https://www.youtube.com/watch?v=UJR1BYjtI7c&feature=youtu.be&t=1m46s) for an idea of the kind of game these questions are meant to support.

In April 2017 basic Spanish support was added.

wikipedia-question-generator is open source under the [MIT License](LICENSE).

Sample usage
------------

Running the command:

```bash
$ wikitrivia --help
```
yields:
```
Usage: wikitrivia [OPTIONS] [TITLES]...

  Generates trivia questions from wikipedia articles. If no titles are
  supplied, pulls from these sample articles:

  'Tony Bennett', 'Gauls', 'Scabbling', 'Henry V, Duke of Carinthia',
  'Ukrainian Women's Volleyball Super League'

Options:
  --lang TEXT        Wikipedia language: en, es
  --output FILENAME  Output to JSON file
  --help             Show this message and exit.
```
And
```bash
$ wikitrivia 'Tony Bennett'
```

yields:

```json
[
  {
    "question": "Bennett is also an accomplished __________, having created works\u2014under the name Anthony Benedetto\u2014that are on permanent public display in several institutions.",
    "answer": "painter", "title": "Tony Bennett",
    "similar_words": ["classic", "classicist", "constructivist", "decorator", "draftsman", "etcher", "expressionist", "illustrator"]
  }
  {
    "question": "He is the __________ of the Frank Sinatra School of the Arts in ..."
  }
]
```

Quickstart
----------

wikipedia-question-generator is a Python 3 project that uses the fantastic [click](http://click.pocoo.org/3/) package to expose itself as a shell command.

You can use the project locally (and quickly) through [Docker](https://www.docker.com/) or a local installation of Python 3.4.

### Installing with Docker

If you just want to run the tool, and don't want to modify it, just pull the latest image from [Docker Hub](https://registry.hub.docker.com/u/beevaenriqueotero/wikipedia-question-generator/):

```bash
$ [sudo] docker pull beevaenriqueotero/wikipedia-question-generator
```

Then, run the image with:

```bash
$ [sudo] docker run beevaenriqueotero/wikipedia-question-generator --help
Usage: wikitrivia [OPTIONS] [TITLES]...

  Generates trivia questions from wikipedia articles. If no titles are
  supplied, pulls from these sample articles:

  'Tony Bennett', 'Python (programming language)', 'Scabbling', 'Ukrainian
  Women's Volleyball Super League'

Options:
  --output FILENAME  Output to JSON file
  --help             Show this message and exit.
```

To make running the container less cumbersome, you can alias the `docker run` command:

```bash
$ alias wikitrivia='[sudo] docker run beevaenriqueotero/wikipedia-question-generator'
$ wikitrivia --help
Usage: wikitrivia [OPTIONS] [TITLES]...
```

If you want to contribute to the tool, you can clone the repo and use [Fig](http://www.fig.sh/) to get started quickly.

### Installing with Python 3.4

Clone the repo, and then use pyvenv-3.4 (or virtualenv) to create a new virtual environment. Then, install the requirements and the NLTK corpora:

```bash
$ pyvenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python -m textblob.download_corpora
```

Install the command line tool so you can use the tool easily:

```bash
$ pip install -e .
```

Now you can run the tool with the command `wikitrivia`.

Advanced usage
--------------

By default, the tool will scrape the hard-coded sample articles listed in the `--help` and return its results to stdout.

### Scraping a specific article

You can point the tool to a specific Wikipedia page by specifying its title:

```bash
$ wikitrivia 'William Shatner'
```

**Be sure to include multi-word titles in quotes, or the tool will treat each word as a separate title.**

### Scraping multiple articles

You can scrape multiple articles at once by providing multiple titles:

```bash
$ wikitrivia 'Leonard Nimoy' 'George Takei' 'Nichelle Nichols'
```

### Outputting to JSON

If you want to take this data elsewhere, you can output the results to a JSON file:

```bash
$ wikitrivia --output scotty.json 'James Doohan'
```

**If you're using `docker run`, by default this will save `scotty.json` inside the container.** Either mount the current directory with the `-v` option or just use fig instead, which mounts the directory as a volume automatically.

Methodology
-----------

More info about original methodology in https://github.com/atbaker/wikipedia-question-generator#methodology
