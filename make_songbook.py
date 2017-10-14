from csv import DictReader

from pylatex import Command, Document, Package, Section, Subsection
from pylatex.utils import italic, NoEscape

from latex_utils import label, link, newline, newpage

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


def make_toc(songlist):
    """Create a table of contents with links to relevent pages."""
    toc = Section('Table of Contents')
    for song in songlist:
        toc.append(link(song.slug, song.title))
        toc.append(newline())
    return toc


def make_songs(songlist):
    """
    Given a list of Song objects, return a list of Sections, each containing
    the lyrics and info for a song.
    """
    output = []
    for song in songlist:
        sect = Section(song.title)
        sect.append(label(song.slug))
        sect.append('By')
        sect.append(italic(song.author))
        sect.append(newline())
        sect.append(song.lyrics())

        output.append(sect)

    return output

if __name__ == '__main__':
    allsongs = songs_from_csv(CSV_PATH)

    doc = Document()
    doc.preamble.append(Package('hyperref'))

    doc.preamble.append(Command('title', 'Maia\'s Songbook'))
    doc.preamble.append(Command('author', 'Maia McCormick'))
    doc.preamble.append(Command('date', NoEscape(r'\today')))
    doc.append(NoEscape(r'\maketitle'))

    toc = make_toc(allsongs)
    doc.append(toc)

    doc.append(newpage())

    for song in make_songs(allsongs):
        doc.append(song)
        doc.append(newpage())

    doc.generate_pdf('songbook', clean_tex=False)
