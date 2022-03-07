from pylatex import Command, Document, Package, Section
from pylatex.basic import NewLine
from pylatex.utils import italic, NoEscape

from song import Song, TAG_PREFIX


class Songbook(Document):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, documentclass='book', **kwargs)
        self._set_up()

    # TODO: fold this into __init__ (or else a Songbook.New() method)
    def _set_up(self):
        """Add packages, set preliminary settings for this doc."""

        # Add packages
        self.preamble.append(Package('hyperref'))
        self.preamble.append(Package('titlesec'))

        # Hide "Chapter 1" etc. (just show chapter name)
        self.preamble.append(NoEscape(r'\titleformat{\chapter}[display]'))
        self.preamble.append(NoEscape(r'{\normalfont\bfseries}{}{0pt}{\Huge}'))

        # Ignore page numbers until we get to the actual body
        self.append(NoEscape(r'\pagenumbering{gobble}'))

        # Title Info
        self.preamble.append(Command('title', 'Maia\'s Songbook'))
        self.preamble.append(Command('author', 'Maia McCormick'))
        self.preamble.append(Command('date', NoEscape(r'\today')))
        self.append(NoEscape(r'\maketitle'))

        # Table of Contents
        self.append(NoEscape(r'\tableofcontents'))

        # Okay, show page numbers again
        self.append(NoEscape(r'\pagenumbering{arabic}'))

    def add_song(self, song: Song):
        """Insert info for the given Song into the Document."""
        self.append(chapter(song.title))
        self.append(label(song.slug))
        self.append('By ')
        self.append(italic(song.author))
        self.append(NewLine())
        self.append(song.lyrics())

    def make_indexes(self, songs_by_tag):
        self.append(chapter('Indexes'))  # ... indicies?
        for tag, songs in songs_by_tag.items():
            with self.create(Section(readable_tag(tag))):
                for song in songs:
                    self.append(link(song.slug, song.title))
                    self.append(NewLine())


# TODO: this should go elsewhere
def readable_tag(tagname):
    """Return human-readable tag name."""
    return tagname[len(TAG_PREFIX):].title()


### UTIL FUNCTIONS ###
def label(labelname):
    s = '\\label{{{labelname}}}'.format(labelname=labelname)
    return NoEscape(s)


def link(labelname, text):
    s = '\\hyperref[{labelname}]{{{text}}}'.format(
        labelname=labelname, text=text
    )
    return NoEscape(s)


def chapter(chapter_name):
    return NoEscape('\\chapter{{{chapter_name}}}'.
        format(chapter_name=chapter_name))

