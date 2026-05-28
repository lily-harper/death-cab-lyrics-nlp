import matplotlib.patches as mpatches
import matplotlib.pyplot as plt 

from src.albums import (
    ALBUM_COLORS,
    BAND_COL_MAP,
    DC_COMPONENT_ALBUMS,
    FAVORITE_SONGS,
    SENTIMENT_ALBUMS,
)


# TF_IDF 

def song_components(
    df,
    ax=None,
    x_col="x",
    y_col="y",
    artist_col="band_name",
    song_col="song_name",
    favorites=None,
    colors=None,
):
    """Plot songs in two-dimensional lyric component space."""
    if ax is None:
        _, ax = plt.subplots(figsize=(7, 5))

    favorites = favorites or FAVORITE_SONGS
    colors = colors or BAND_COL_MAP

    artists = df[artist_col].dropna().unique()

    for artist in artists:
        subset = df[df[artist_col] == artist]
        ax.scatter(
            subset[x_col],
            subset[y_col],
            label=artist,
            alpha=0.65,
            edgecolors="white",
            s=50,
            color=colors.get(artist),
        )

    for _, row in df.iterrows():
        if row[song_col] in favorites:
            ax.annotate(
                row[song_col],
                (row[x_col], row[y_col]),
                fontsize=8,
                color="black",
                bbox=dict(facecolor="white", alpha=0.7),
            )
    ax.set_title("Songs Vectorized with TF-IDF in SVD Space")
    ax.set_xlabel("SVD Component 1")
    ax.set_ylabel("SVD Component 2")
    ax.legend()

    return ax

def song_components_dc_album(df):
    dc = df[df["band_name"] == "Death Cab for Cutie"]

    dc = dc[dc["album"].isin(DC_COMPONENT_ALBUMS)]

    albums = dc["album"].unique()

    for album in albums:
        subset = dc[dc["album"] == album]

        plt.scatter(subset["x"], subset["y"], 
                    label=album, edgecolors= "white", 
                    alpha = 0.65, s = 50)

    plt.xlim(-.1, .25)
    plt.ylim(-.1, .45)

    plt.suptitle("2d Projection of Song Lyric Similarity")
    plt.title("Death Cab Songs Vectorized with TF-IDF in PCA Space")
    plt.xlabel("PCA Comp. 1")
    plt.ylabel("PCA Comp 2")
    plt.legend()
    plt.show()

# vader stuff 

def ben_gibbard_boxplot(df):
    df.boxplot(
        column = "sentiment",
        by = "band_name",
        grid = False
    )
    plt.suptitle(" ")
    plt.title("Sentiment in Ben Gibbards Lyrics by Musical Group")
    plt.xlabel("Musical Group")
    plt.ylabel("VADER Sentiment")

    plt.show()

def vader_album(df):
    dc = df[df["band_name"] == "Death Cab for Cutie"]
    dc = dc[df["album"].isin(SENTIMENT_ALBUMS)]

    album_sentiment = (
        dc.groupby("album")["sentiment"]
        .mean()
        .sort_values()
    )

    colors = [ALBUM_COLORS.get(album, "slategray") for album in album_sentiment.index]
    album_sentiment.plot(kind="bar", color=colors)

    plt.title("Sentiment across DCFC Albums")
    plt.xlabel("Album")
    plt.ylabel("Average VADER Sentiment")

    plt.xticks(rotation = 45, ha= "right")
    plt.axhline(y=0, color = "black", linewidth = .75)
    plt.figtext(.5,-.2,
        "(Colors based on album art)")
    plt.show()

def vader_chart(df):
    subset = df[df["album"].isin(SENTIMENT_ALBUMS)]

    sentiment_album = (
        subset.groupby(["band_name", "album"], as_index = False)["sentiment"]
        .mean()
    )

    sentiment_album["color"] = sentiment_album["band_name"].map(BAND_COL_MAP)

    plot_df = sentiment_album.sort_values("sentiment")
    plt.bar(
        plot_df["album"],
        plot_df["sentiment"],
        color=plot_df["color"]
    )

    legend_handles = [
        mpatches.Patch(color=color, label=band)
        for band, color in BAND_COL_MAP.items()
    ]

    plt.xticks(rotation=45, ha = "right")
    plt.legend(handles = legend_handles, title = "Musical Group")
    plt.ylabel("Average VADER Sentiment")
    plt.title("Average Sentiment by Album")

    plt.show()