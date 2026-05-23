import pandas as pd 
import lyricsgenius 
import os 
from dotenv import load_dotenv

from src.paths import RAW_DATA_PATH, save_data

def genius_token(env_var_name): # 
    GENIUS_ACCESS_TOKEN = os.getenv(env_var_name)

    if not GENIUS_ACCESS_TOKEN:
        raise ValueError("missing GENIUS_ACCESS_TOKEN in .env file")

    genius = lyricsgenius.Genius(GENIUS_ACCESS_TOKEN)

    return genius

def pull_settings(genius):
    genius.skip_non_songs = True
    genius.exclude_terms = ["(Live)", "(Remix)", "Remix", 
                            "Live", "(Demo)", "(Band Demo)", "Demo", "Acoustic", 
                            "(Acoustic)"]

    genius.remove_section_headers = True
    genius.timeout = 15

    return genius

def get_release_year(song):
    components = getattr(song, "release_date_components", None)

    if components is None:
        body = getattr(song, "_body", {})
        components = body.get("release_date_components")

    if components and components.get("year"):
        return components["year"]

    release_date = getattr(song, "release_date", None)

    if release_date is None:
        body = getattr(song, "_body", {})
        release_date = body.get("release_date")

    if release_date:
        parsed_date = pd.to_datetime(release_date, errors="coerce")
        if not pd.isna(parsed_date):
            return parsed_date.year

    return None

def api_pull(genius):

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
            print(f"Could not find artist: {name}")
            continue

        for song in artist.songs:
            print(f"  - {song.title}")

            lyrics = song.lyrics if song.lyrics else None

            rows.append({"band_name": name,
                        "album": song.album['name'] if song.album else None,
                        "song_name": song.title,
                        "release_year": get_release_year(song),
                        "lyrics":lyrics,
                        "genius_url":song.url
                        })
            
    df = pd.DataFrame(rows)

    return df 

def main():

    load_dotenv()

    genius = genius_token("GENIUS_ACCESS_TOKEN")
    genius = pull_settings(genius)

    df = api_pull(genius)
    save_data(df, RAW_DATA_PATH, output="csv")

if __name__== "__main__":
    main()