#! /usr/bin/env python

# pylint:disable=redefined-outer-name

from csv import DictReader
from collections import defaultdict
from typing import Dict, List

from pylatex import Command, Document, Package, Section
from pylatex.basic import NewLine
from pylatex.utils import italic, NoEscape

from latex import chapter, label, link, Songbook
from song import songs_from_csv

# TODO: markdown-to-latex for my lyric files?

CSV_PATH = 'songinfo.csv'
TITLE_KEY = 'title'
AUTHOR_KEY = 'author'
LYRICPATH_KEY = 'lyricpath'
TAG_PREFIX = 'tag_'


if __name__ == '__main__':
    # TODO: it'd be nice and shiny if these were all methods on the document
    allsongs, songs_by_tag = songs_from_csv(CSV_PATH)

    document = Songbook()

    for song in allsongs:
        document.add_song(song)

    document.make_indexes(songs_by_tag)

    document.generate_pdf('songbook', clean_tex=False)
