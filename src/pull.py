import pandas as pd 
import lyricsgenius 
import os 
from dotenv import load_dotenv

load_dotenv()

GENIUS_ACCESS_TOKEN = os.getenv("GENIUS_ACCESS_TOKEN")

if not GENIUS_ACCESS_TOKEN:
    raise ValueError("missing GENIUS_ACCESS_TOKEN in .env file")

genius = lyricsgenius.Genius(GENIUS_ACCESS_TOKEN)

genius.skip_non_songs = True
genius.exclude_terms = ["(Live)", "(Remix)", "Remix", 
                        "Live", "(Demo)", "(Band Demo)", "Demo", "Acoustic", 
                        "(Acoustic)"]

genius.remove_section_headers = True
genius.timeout = 15

artists = [
    "Death Cab for Cutie",
    "The Postal Service",
    "Benjamin Gibbard"
]

rows = []

for name in artists:
    print(f"Pulling songs for {name}")

    artist = genius.search_artist(
        name,
        max_songs = None,
        sort="title"
    )

    if artist is None:
        print(f"Could not find artist{name}")
        continue

    for song in artist.songs:
        print(f"  - {song.title}")

        lyrics = song.lyrics if song.lyrics else None

        rows.append({"band_name": name,
                     "album": song.album['name'] if song.album else None,
                     "song_name": song.title,
                     "lyrics":lyrics,
                     "genius_url":song.url
                     })
        
df = pd.DataFrame(rows)

df.to_csv("data/raw/raw_lyrics.csv", index = False)

print("\n Saved dataset.")
print(df.shape)