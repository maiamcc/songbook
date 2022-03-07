from csv import DictReader
from collections import defaultdict
from typing import Dict, List, Optional

CSV_PATH = 'songinfo.csv'
TITLE_KEY = 'title'
AUTHOR_KEY = 'author'
LYRICPATH_KEY = 'lyricpath'
TAG_PREFIX = 'tag_'


class Song:
    """Contains relevant information about a single song."""
    def __init__(self, title, author, lyricpath, tags: Optional[List[str]] = None):
        self.title = title
        self.author = author
        self.lyricpath = lyricpath
        self.tags = [readable_tag(tag) for tag in tags] if tags else []

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


class SongCollection:
    """A way to describe a bunch of songs--largely for ease of ordering, grouping by tag, etc."""

    @classmethod
    def from_csv(cls, csv_path: str) -> "SongCollection":
        """Parse provided CSV into Song objects."""
        songs = []
        tags = []

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
                    lyricpath=row[LYRICPATH_KEY],

                    # any non-falsey value counts as a hit for this tag
                    tags=[tag for tag in tags if row.get(tag)]
                )
                songs.append(new_song)

        return cls(songs)

    def __init__(self, songs: List[Song]):
        self.songs = songs
        self.by_tag = defaultdict(list)

        for song in self.songs:
            for tag in song.tags:
                self.by_tag[tag].append(song)

    # TODO: bet there's a fancy way to put the iterator straight on the class so I can
    #   do "for song in my_collection" rather than "for song in my_collection.songs"
    #   def __iter__(self): ...


def readable_tag(tagname):
    """Return human-readable tag name."""
    return tagname[len(TAG_PREFIX):].title()
