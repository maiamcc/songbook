from csv import DictReader
from collections import defaultdict
from typing import Dict, List

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
