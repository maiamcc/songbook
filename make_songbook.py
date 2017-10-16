from csv import DictReader

from pylatex import Command, Document, Package
from pylatex.basic import NewLine
from pylatex.utils import italic, NoEscape

from latex_utils import chapter, label, link

# TODO: markdown-to-latex for my lyric files?

CSV_PATH = 'songinfo.csv'
TITLE_KEY = 'title'
AUTHOR_KEY = 'author'
LYRICPATH_KEY = 'lyricpath'

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


def songs_from_csv(csv_path):
    """Parse provided CSV into Song objects."""
    songs = []
    with open(csv_path) as csvfile:
        reader = DictReader(csvfile)
        for row in reader:
            new_song = Song(
                            title=row[TITLE_KEY],
                            author=row[AUTHOR_KEY],
                            lyricpath=row[LYRICPATH_KEY]
                        )
            songs.append(new_song)

    return songs


def add_song_to_doc(doc, song):
    """Insert info for the given Song into the Document."""
    doc.append(chapter(song.title))
    # doc.append(label(song.slug))
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

if __name__ == '__main__':
    allsongs = songs_from_csv(CSV_PATH)

    document = set_up(Document(documentclass='book'))

    for song in allsongs:
        document = add_song_to_doc(document, song)

    document.generate_pdf('songbook', clean_tex=False)
