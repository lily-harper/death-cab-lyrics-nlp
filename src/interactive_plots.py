
import plotly.express as px

from src.albums import (
    ALBUM_COLORS,
    BAND_COL_MAP,
    DC_COMPONENT_ALBUMS,
    FAVORITE_SONGS,
    SENTIMENT_ALBUMS,
)

def yearly_sentiment(df):
    df = df.copy()

    yearly_df = (
        df.groupby(["release_year", "band_name"], as_index = False)
        .agg(
            mean_sentiment = ("sentiment", "mean"),
            median_sentiment = ("sentiment", "median"),
            songs = ("song_name", "count")))
    
    return yearly_df
    

def sentiment_per_year_plotly(df):
    yearly_df = yearly_sentiment(df)
    fig = px.line(
        yearly_df,
        x = "release_year",
        y = "mean_sentiment",
        color = "band_name",
        markers = True,
        hover_data={
            "release_year": True,
            "band_name": True,
            "mean_sentiment": ":.3f",
            "songs": True
        },
        title = "Average VADER Sentiment by Release Year per Band",
        labels = {
            "release_year": "Release Year",
            "mean_sentiment": "Average VADER sentiment",
            "band_name": "Artist"
        }
    )

    fig.add_hline(y = 0, line_dash = "dash", line_color = "grey")
    fig.update_layout(template = "plotly_white", hovermode = "x unified")
    
    return fig

def song_level_vader(df):
    fig = px.scatter(
        df, 
        x = "release_year",
        y = "sentiment",
        color = "band_name",
        hover_name = "song_name",
        hover_data={
            "album":True,
            "release_year": True,
            "sentiment": ":.3f",
            "band_name":True
        },
        marginal_y="box",
        title = "Song Level VADER Sentiment by Release Year",
        labels = {
            "release_year": "Release year",
            "sentiment": "VADER Sentiment",
            "band_name":"Artist",
            "album": "Album"
        }
    )

    fig.add_hline(y= 0, line_dash = "dash", line_color = "grey")

    album_annotations = [
        "Give Up",
        "Plans",
        "Kintsugi",
    ]

    for album in album_annotations:
        album_rows = df[df["album"] == album]

        year = int(album_rows["release_year"].iloc[0])

        fig.add_annotation(
            x=year,
            y=1.08,
            text=album,
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1,
            arrowcolor="gray",
            ax=0,
            ay=-30,
            bgcolor="white",
            font={"size": 10},
    )
        
    fig.update_traces(marker={"size": 9, "opacity": 0.75})
    fig.update_layout(template="plotly_white", yaxis={"range": [-1.05, 1.18]})
    
    return fig 
