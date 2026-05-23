import pandas as pd 
import numpy as np
import re

from src.lyric_preprocessing import (remove_missing_lyrics, remove_versions,
                                     remove_covers, clean_text,
                                     shorten_album_names,
                                     fill_missing_albums,
                                     assign_album_majority_year,
                                     convert_column_types)

from src.paths import RAW_DATA_PATH, CLEAN_DATA_PATH, save_data

def summary(df: pd.DataFrame, raw = False):
    if raw: 
        print(f"There are {df.shape[0]} rows and {df.shape[1]} columns \n in the dataframe before cleaning")
        print("Each band has, before cleaning, this many observations \n")
        print(df["band_name"].value_counts())
    else:
        print(f"There are {df.shape[0]} rows and {df.shape[1]} columns \n in the dataframe after cleaning")
        print("Each band has, after cleaning, this many observations \n")
        print(df["band_name"].value_counts())

def clean_lyrics(df: pd.DataFrame) -> pd.DataFrame:
    print("Removing rows with no lyrics...")
    df = remove_missing_lyrics(df)

    print("Removing covers...")
    df = remove_covers(df)

    print("Cleaning text")
    df["song_name_clean"] = df["song_name"].apply(clean_text)
    df["lyrics_clean"] = df["lyrics"].apply(clean_text)

    print("Removing duplicate versions...")
    df = remove_versions(df)

    print("Shortening album names...")
    df = shorten_album_names(df)

    print("Assigning album majority years...")
    df = assign_album_majority_year(df)

    print("Filling missing albums...")
    df = fill_missing_albums(df)

    df = convert_column_types(df, 
                              int_cols=["release_year"],
                              string_cols=["song_name_clean", "song_name",
                                           "lyrics_clean", "lyrics",
                                           "genius_url"],
                              category_cols=["band_name", "album"])

    return df

def main():
    df = pd.read_csv(RAW_DATA_PATH)
    summary(df, raw = True)

    df = clean_lyrics(df)

    save_data(df, CLEAN_DATA_PATH, output = "parquet")
    summary(df)

if __name__ == "__main__":
    main()
