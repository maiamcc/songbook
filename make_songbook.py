# pylint:disable=redefined-outer-name

from csv import DictReader
from collections import defaultdict
from typing import Dict, List

from pylatex import Command, Document, Package, Section
from pylatex.basic import NewLine
from pylatex.utils import italic, NoEscape

from latex_utils import chapter, label, link

# TODO: markdown-to-latex for my lyric files?

CSV_PATH = 'songinfo.csv'
TITLE_KEY = 'title'
AUTHOR_KEY = 'author'
LYRICPATH_KEY = 'lyricpath'
TAG_PREFIX = 'tag_'

class Song():
    """Contains relevant information about a single song."""
    def __init__(self, title, author, lyricpath):
        self.title = title
        self.author = author
        self.lyricpath = lyricpath

        # for later
        # self.vocalrange = vocalrange
        # self.categories = categories

    def lyrics(self):
        """Get lyrics from file specified in 'lyricpath'."""
        with open(self.lyricpath) as lyricfile:
            return lyricfile.read()


    @property
    def slug(self):
        """Return slug generated from Title suitable for use as link label."""
        return ''.join(char.lower() for char in self.title if char.isalnum())


def songs_from_csv(csv_path: str) -> (List[Song], Dict[str, List[Song]]):
    """Parse provided CSV into Song objects."""
    songs = []
    tags = []
    songs_by_tag = defaultdict(list)

    with open(csv_path) as csvfile:
        reader = DictReader(csvfile)
        for row in reader:

            # first run: figure out which columns are tags ("tag_" prefix)
            if not tags:
                for k in row.keys():
                    if k.startswith(TAG_PREFIX):
                        tags.append(k)
            new_song = Song(
                            title=row[TITLE_KEY],
                            author=row[AUTHOR_KEY],
                            lyricpath=row[LYRICPATH_KEY]
                        )
            songs.append(new_song)

            # Add song to list for any tags
            for tag in tags:
                if row.get(tag):
                    # any non-falsey value counts as a hit for this tag
                    songs_by_tag[tag].append(new_song)

    # TODO: sort songs by title before returning
    return songs, songs_by_tag


def add_song_to_doc(doc, song):
    """Insert info for the given Song into the Document."""
    doc.append(chapter(song.title))
    doc.append(label(song.slug))
    doc.append('By ')
    doc.append(italic(song.author))
    doc.append(NewLine())
    doc.append(song.lyrics())

    return doc


def set_up(doc):
    """Add packages, set preliminary settings for this doc."""
    # Add packages
    doc.preamble.append(Package('hyperref'))
    doc.preamble.append(Package('titlesec'))

    # Hide "Chapter 1" etc. (just show chapter name)
    doc.preamble.append(NoEscape(r'\titleformat{\chapter}[display]'))
    doc.preamble.append(NoEscape(r'{\normalfont\bfseries}{}{0pt}{\Huge}'))

    # Ignore page numbers until we get to the actual body
    doc.append(NoEscape(r'\pagenumbering{gobble}'))

    # Title Info
    doc.preamble.append(Command('title', 'Maia\'s Songbook'))
    doc.preamble.append(Command('author', 'Maia McCormick'))
    doc.preamble.append(Command('date', NoEscape(r'\today')))
    doc.append(NoEscape(r'\maketitle'))

    # Table of Contents
    doc.append(NoEscape(r'\tableofcontents'))

    # Okay, show page numbers again
    doc.append(NoEscape(r'\pagenumbering{arabic}'))

    return doc


def make_indexes(doc, songs_by_tag):
    doc.append(chapter('Indexes')) # ... indicies?
    for tag, songs in songs_by_tag.items():
        with doc.create(Section(readable_tag(tag))):
            for song in songs:
                doc.append(link(song.slug, song.title))
    return doc


def readable_tag(tagname):
    """Return human-readable tag name."""
    return tagname[len(TAG_PREFIX):].title()


if __name__ == '__main__':
    # TODO: it'd be nice and shiny if these were all methods on the document
    allsongs, songs_by_tag = songs_from_csv(CSV_PATH)

    document = set_up(Document(documentclass='book'))

    for song in allsongs:
        document = add_song_to_doc(document, song)

    document = make_indexes(document, songs_by_tag)

    document.generate_pdf('songbook', clean_tex=False)
