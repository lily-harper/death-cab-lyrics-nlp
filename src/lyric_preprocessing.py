import numpy as np
import pandas as pd 
import re

def remove_missing_lyrics(df):
    df = df.dropna(subset=["lyrics"])
    df = df[df["lyrics"].str.len() > 0]

    return df 

def remove_versions(df):
    """This removes rows where there were alternate 
    versions or styles of the song 
    """
    exclude = ["band demo","alternate","demo", "acoustic",  
           "concert", "remix", "edit", "original", 
           "the wiltern", "the fillmore", "dub", "single",
           "live", "seattle", "version", "mix", "cover", "version",
           "kfog", "kexp", "rolling stone"]
    
    leave = "|".join(exclude)
    df = df[~df["song_name_clean"].str.contains(leave, case = False, na=False)]

    df = df.drop_duplicates(subset = ['song_name_clean'])
            
    return df 

def clean_text(text: str) -> str:
    if pd.isna(text):
        return ""

    text = str(text).lower().strip()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text)

    return text

def shorten_album_names(
    df,
    album_col="album",
    replacements=None,
) -> pd.DataFrame:
    """Normalize album names by removing edition labels."""
    df = df.copy()
    replacements = replacements or {}

    albums = df[album_col].astype("string").str.strip()
    albums = albums.mask(albums.eq(""))

    albums = albums.str.replace(r"\s*\([^)]*\)\s*$", "", regex=True)
    albums = albums.str.strip()
    albums = albums.replace(replacements)

    df[album_col] = albums

    return df

def fill_missing_albums(
    df,
    album_col="album",
    value="Single",
) -> pd.DataFrame:
    """Fill missing or blank album names with a label."""
    df = df.copy()

    albums = df[album_col].astype("string").str.strip()
    df[album_col] = albums.mask(albums.isna() | albums.eq(""), value)

    return df

def assign_album_majority_year(
    df,
    album_col="album",
    year_col="release_year",
) -> pd.DataFrame:
    """Set each album's release year to its most common non-missing year."""
    df = df.copy()

    years = pd.to_numeric(df[year_col], errors="coerce")
    albums = df[album_col].astype("string").str.strip()
    has_album = albums.notna() & albums.ne("")

    def majority_year(album_years):
        album_years = album_years.dropna()

        if album_years.empty:
            return pd.NA

        return album_years.mode().iloc[0]

    df[year_col] = years
    df.loc[has_album, year_col] = years.loc[has_album].groupby(
        albums.loc[has_album]
    ).transform(majority_year)

    return df

def convert_column_types(df,
    int_cols=None,
    category_cols=None,
    string_cols=None,
    errors="coerce") -> pd.DataFrame:
    
    int_cols = int_cols or []
    category_cols = category_cols or []
    string_cols = string_cols or []

    for col in int_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors=errors).astype("Int64")

    for col in category_cols:
        if col in df.columns:
            df[col] = df[col].astype("category")

    for col in string_cols:
        if col in df.columns:
            df[col] = df[col].astype("string")

    return df


def remove_covers(df):
    covers = [
        "Against All Odds (Take a Look at Me Now)",
        "All Is Full of Love",
        "And I Love Him",
        "Bad Reputation",
        "Choir Vandals",
        "Christmas (Baby Please Come Home)",
        "Dream Scream",
        "Earth Angel",
        "Fall On Me",
        "Filler",
        "Flirted With You All My Life",
        "Fortunate Son (feat. Sean Nelson)",
        "Grow Old with Me",
        "Indian Summer",
        "Is This Music",
        "Joga",
        "Keep Yourself Warm",
        "King of Carrot Flowers, Pt. 1",
        "Love Song",
        "Metal Baby",
        "Metal Heart",
        "My Backwards Walk",
        "Our Secret",
        "Rockin' Chair",
        "Satan",
        "St. Swithin's Day",
        "Start Again",
        "Suddenly Everything Has Changed",
        "Sweet and Tender Hooligan (The Smiths cover)",
        "The Concept",
        "This Charming Man",
        "Waterfalls",
        "World Shut Your Mouth",
    ]

    song_titles = df["song_name"]
    df = df[~song_titles.isin(covers)]

    return df 


def add_lyrics_no_stopwords(
    df,
    text_col="lyrics_clean",
    output_col="lyrics_no_stopwords",
    extra_stopwords=None,
) -> pd.DataFrame:
    """Create a lyric column with NLTK and custom stopwords removed."""
    from src.count import get_stopwords

    df = df.copy()
    stop_words = get_stopwords(extra_stopwords)

    def remove_stopwords(text):
        if pd.isna(text):
            return ""

        tokens = str(text).split()
        tokens = [word for word in tokens if word not in stop_words]

        return " ".join(tokens)

    df[output_col] = df[text_col].apply(remove_stopwords)

    return df
