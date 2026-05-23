import re

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from src.count import album_word_counts, plot_top_words
from src.paths import CLEAN_DATA_PATH, WORD_COUNT_FIGURES_DIR
from src.albums import FAVORITE_ALBUMS, ALBUM_COLORS


def slugify(value):
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


def save_top_words_plot(df, output_path, album=None, n=20, color="slategray"):
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(7, 5))
    plot_top_words(df, album=album, n=n, col=color, ax=ax)
    fig.tight_layout()
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved {output_path}")


def save_word_count_figures(df, min_songs=3, n=20):
    albums = album_word_counts(df)
    albums = albums[
        (albums["songs"] >= min_songs)
        & (albums["album"].isin(FAVORITE_ALBUMS))
    ]

    plots_saved = 0

    save_top_words_plot(
        df,
        WORD_COUNT_FIGURES_DIR / "all_lyrics_top_words.png",
        album=None,
        n=n,
        color="slategray",
    )
    plots_saved += 1

    for album in albums["album"]:
        save_top_words_plot(
            df,
            WORD_COUNT_FIGURES_DIR / f"{slugify(album)}_top_words.png",
            album=album,
            n=n,
            color=ALBUM_COLORS.get(album, "slategray"),
        )
        plots_saved += 1
    
    return plots_saved


def main():
    print("Some figures")
    df = pd.read_parquet(CLEAN_DATA_PATH)
    n = save_word_count_figures(df)
    print(f"Saved {n} plots to {WORD_COUNT_FIGURES_DIR}")


if __name__ == "__main__":
    main()
