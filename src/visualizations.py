import matplotlib.patches as mpatches
import matplotlib.pyplot as plt 

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


