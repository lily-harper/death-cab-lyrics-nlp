import matplotlib.patches as mpatches
import matplotlib.pyplot as plt 

favs = [
    "Asphalt Meadows",
    "Codes and Keys",
    "Kintsugi",
    "Narrow Stairs",
    "Plans",
    "Transatlanticism (2013 Reissue)",
    "Something About Airplanes",
    "Thank You for Today",
]

cols = [
    "steelblue", "grey", "darkgrey", "gold", 
    "darkred", "royalblue", "tan"
]

# TF_IDF 

def song_components(df):
    artists = df["band_name"].unique()

    for artist in artists:
        subset = df[df["band_name"] == artist]
        plt.scatter(subset["x"], subset["y"], 
                    label=artist, alpha = 0.65,
                    edgecolors= "white",
                    s = 50)

    favs = ["Stable Song", 
            "Transatlanticism", 
            "Lily", # biased toward this one :) 
            "Such Great Heights",
            "The Ghosts of Beverly Drive"]

    for i, row in df.iterrows():
        if row["song_name"] in favs:
            plt.annotate(
                row["song_name"],
                (row["x"], row["y"]),
                fontsize = 10
            )

    plt.legend()
    plt.show()

def song_components_dc_album(df):
    
    favs = [
    "Asphalt Meadows",
    "Codes and Keys",
    "Kintsugi",
    "Narrow Stairs",
    "Plans",
    "Transatlanticism (2013 Reissue)",
    "Something About Airplanes",
    "Thank You for Today",
]
    dc = df[df["band_name"] == "Death Cab for Cutie"]

    dc = dc[dc["album"].isin(favs)]

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
    dc = dc[df["album"].isin(favs)]

    album_sentiment = (
        dc.groupby("album")["sentiment"]
        .mean()
        .sort_values()
    )

    album_sentiment.plot(kind="bar", color = cols)

    plt.title("Sentiment across DCFC Albums")
    plt.xlabel("Album")
    plt.ylabel("Average VADER Sentiment")

    plt.xticks(rotation = 45, ha= "right")
    plt.axhline(y=0, color = "black", linewidth = .75)
    plt.figtext(.5,-.2,
        "(Colors based on album art)")
    plt.show()

def vader_chart(df):
    
    fav_albums = [
        "Plans",
        "Transatlanticism (2013 Reissue)",
        "Narrow Stairs ",
        "Kintsugi",
        "Give Up (10th Anniversary Edition)",
        "Former Lives",
        "Something About Airplanes",
        "The Photo Album (Deluxe Edition)",
        "Codes and Keys"
    ]

    col_map = { 
        "Death Cab for Cutie": "steelblue",
        "Benjamin Gibbard": "navy",
        "The Postal Service": "slategrey"}

    subset = df[df["album"].isin(fav_albums)]

    sentiment_album = (
        subset.groupby(["band_name", "album"], as_index = False)["sentiment"]
        .mean()
    )

    sentiment_album["color"] = sentiment_album["band_name"].map(col_map)

    plot_df = sentiment_album.sort_values("sentiment")
    plt.bar(
        plot_df["album"],
        plot_df["sentiment"],
        color=plot_df["color"]
    )

    legend_handles = [
        mpatches.Patch(color="steelblue", label="Death Cab for Cutie"),
        mpatches.Patch(color="navy", label="Benjamin Gibbard"),
        mpatches.Patch(color="slategrey", label="The Postal Service")
    ]

    plt.xticks(rotation=45, ha = "right")
    plt.legend(handles = legend_handles, title = "Musical Group")
    plt.ylabel("Average VADER Sentiment")
    plt.title("Average Sentiment by Album")

    plt.show()


