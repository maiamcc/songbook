#! /usr/bin/env python

# pylint:disable=redefined-outer-name

from latex import Songbook
from song import SongCollection

# TODO: markdown-to-latex for my lyric files?

CSV_PATH = 'songinfo.csv'


if __name__ == '__main__':
    # TODO: it'd be nice and shiny if these were all methods on the document
    songs = SongCollection.from_csv(CSV_PATH)

    document = Songbook()

    for song in songs.songs:
        document.add_song(song)

    document.make_indexes(songs.by_tag)

    document.generate_pdf('songbook', clean_tex=False)
