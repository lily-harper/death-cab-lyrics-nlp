import re

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from src.albums import FAVORITE_ALBUMS, ALBUM_COLORS
from src.count import album_word_counts, plot_top_words
from src.paths import (
    CLEAN_DATA_PATH,
    FIGURES_DIR,
    PLOTLY_FIGURES_DIR,
    PLOTTING_DATA_PATH,
    WORD_COUNT_FIGURES_DIR,
)
from src.visualizations import song_components
from src.interactive_plots import sentiment_per_year_plotly, song_level_vader


SONG_COMPONENTS_FIGURE_PATH = FIGURES_DIR / "song_components.png"

def slugify(value):
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")


def save_plot(plot_func, df, output_path, figsize=(7, 5), dpi=300, **kwargs):
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=figsize)
    plot_func(df, ax=ax, **kwargs)
    fig.tight_layout()
    fig.savefig(output_path, dpi=dpi, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved {output_path}")


def save_top_words_plot(df, output_path, album=None, n=20, color="slategray"):
    save_plot(
        plot_top_words,
        df,
        output_path,
        album=album,
        n=n,
        col=color,
    )


def save_song_components_figure(df, output_path=SONG_COMPONENTS_FIGURE_PATH):
    save_plot(
        song_components,
        df,
        output_path,
        figsize=(7, 5),
    )


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


def save_all_figures(df_clean, df_plotting=None):
    plots_saved = save_word_count_figures(df_clean)

    if df_plotting is not None:
        save_song_components_figure(df_plotting)
        plots_saved += 1

        plots_saved += save_interactive_figures(df_plotting)

    return plots_saved



# interactive plots

SENTIMENT_YEAR_HTML_PATH = PLOTLY_FIGURES_DIR / "sentiment_per_year.html"
SONG_LEVEL_VADER_HTML_PATH = PLOTLY_FIGURES_DIR / "song_level_vader.html"

def save_plotly_figure(fig_func, df, output_path, **kwargs):
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig = fig_func(df, **kwargs)
    fig.write_html(output_path)

    print(f"Saved {output_path}")
    
    return 1 

def save_interactive_figures(df_plotting):
    plots_saved = save_plotly_figure(
        sentiment_per_year_plotly,
        df_plotting,
        SENTIMENT_YEAR_HTML_PATH,
    )
    plots_saved += save_plotly_figure(
        song_level_vader,
        df_plotting,
        SONG_LEVEL_VADER_HTML_PATH,
    )

    return plots_saved

def main():
    print("Some figures")
    df = pd.read_parquet(CLEAN_DATA_PATH)
    df_plotting = pd.read_parquet(PLOTTING_DATA_PATH)
    n = save_all_figures(df, df_plotting)
    print(f"Saved {n} plots to {FIGURES_DIR}")

if __name__ == "__main__":
    main()
