#! /usr/bin/env python

# pylint:disable=redefined-outer-name

from latex import Songbook
from song import songs_from_csv

# TODO: markdown-to-latex for my lyric files?

CSV_PATH = 'songinfo.csv'


if __name__ == '__main__':
    # TODO: it'd be nice and shiny if these were all methods on the document
    allsongs, songs_by_tag = songs_from_csv(CSV_PATH)

    document = Songbook()

    for song in allsongs:
        document.add_song(song)

    document.make_indexes(songs_by_tag)

    document.generate_pdf('songbook', clean_tex=False)
