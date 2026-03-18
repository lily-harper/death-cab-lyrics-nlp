import numpy as np
import pandas as pd 

def remove_missing_lyrics(df):
    df = df.dropna(subset=["lyrics"])
    return df 

def remove_versions(df):
    """This removes rows where there were alternate 
    versions or styles of the song 
    """
    exclude = ["band demo","alternate","demo", "acoustic",  
           "concert", "remix", "edit", "original", 
           "the wiltern", "the fillmore", "dub", "single",
           "live", "seattle", "version", "mix", "cover"]

    leave = "|".join(exclude)
    df = df[~df["song_name"].str.contains(leave, case = False, na=False)]

    return df 

def lowercase_rows(df):
    low = ["song_name", "lyrics"]
    for col in low:
        df[col] = df[col].str.lower()
         
    return df 


def remove_covers(df):
    covers = ["christmas (baby please come home)", # darlene love
          "fortunate son (feat. sean nelson)", # ccr 
          "king of carrot flowers, pt. 1" # nuetral milk hotel :) 
          ] 

    df = df[~df["song_name"].isin(covers)]  

    return df 
