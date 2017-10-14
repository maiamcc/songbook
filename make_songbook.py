from pylatex import Command, Document, Package, Section, Subsection
from pylatex.utils import italic, NoEscape

from latex_utils import label, link, newline, newpage

# TODO: markdown-to-latex for my lyric files?

class Song():
    """Contains relevant information about a single song."""
    def __init__(self, title, author, vocalrange, lyricpath, categories):
        self.title = title
        self.author = author
        self.vocalrange = vocalrange
        self.lyricpath = lyricpath
        self.categories = categories

    def lyrics(self):
        """Get lyrics from file specified in 'lyricpath'."""
        return "la la laaaa"

    @property
    def slug(self):
        """Return slug generated from Title suitable for use as link label."""
        return ''.join(char.lower() for char in self.title if char.isalnum())


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
    song1 = Song('Do Re Mi', 'Julie Andrews', 'do - do', 'doremi', ['foo', 'bar'])
    song2 = Song('Eye of the Tiger', 'Calvin and Hobbes', 'la - la', 'eye_of_tiger', ['bar', 'baz'])
    allsongs = [song1, song2]

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

    doc.generate_pdf('songbook', clean_tex=False)
