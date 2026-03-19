import numpy as np
import pandas as pd 
import re

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

    df["lyrics_clean"] = df["lyrics"].str.lower()
    df["song_lower"] = df["song_name"].str.lower()
         
    return df 


def remove_covers(df):
    covers = ["christmas (baby please come home)", # darlene love
          "fortunate son (feat. sean nelson)", # ccr 
          "king of carrot flowers, pt. 1", # nuetral milk hotel :) 
          "Flirted With You All My Life	"
          ] 

    df = df[~df["song_name"].isin(covers)]  

    return df 

def strip_lyrics(text):
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text 