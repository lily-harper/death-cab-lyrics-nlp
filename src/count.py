from collections import Counter

import pandas as pd


CUSTOM_STOPWORDS = {
    "bop",
    "bah",  # sorry to the sound of settling
    "whoa",
    "woah",
    "oohwhaho", "ohhohh",
    "ba", "oh"
}


def get_stopwords(extra_stopwords=None):
    """Return the stopword set used for lyric word counts."""
    from nltk.corpus import stopwords

    extra_stopwords = extra_stopwords or set()
    return set(stopwords.words("english")).union(CUSTOM_STOPWORDS, extra_stopwords)


def word_counts(
    df,
    album=None,
    text_col="lyrics_clean",
    album_col="album",
    remove_stopwords=True,
    extra_stopwords=None,
) -> pd.DataFrame:
    """Count words in lyrics and return a table sorted by frequency."""
    if album is None:
        filter_df = df
    else:
        filter_df = df[df[album_col] == album]

    tokens = " ".join(filter_df[text_col].dropna().astype(str)).split()

    if remove_stopwords:
        stop_words = get_stopwords(extra_stopwords)
        tokens = [word for word in tokens if word not in stop_words]

    counts = Counter(tokens)

    return pd.DataFrame(counts.most_common(), columns=["word", "count"])


def top_words(
    df,
    album=None,
    n=20,
    text_col="lyrics_clean",
    album_col="album",
    remove_stopwords=True,
    extra_stopwords=None,
) -> pd.DataFrame:
    """Return the top n words for all lyrics or one album."""
    counts = word_counts(
        df,
        album=album,
        text_col=text_col,
        album_col=album_col,
        remove_stopwords=remove_stopwords,
        extra_stopwords=extra_stopwords,
    )

    return counts.head(n)


def album_word_counts(
    df,
    text_col="lyrics_clean",
    album_col="album",
) -> pd.DataFrame:
    """Return total word counts and song counts by album."""
    word_counts_by_song = df[text_col].fillna("").astype(str).str.split().str.len()

    album_counts = (
        df.assign(word_count=word_counts_by_song)
        .groupby(album_col, observed=False)
        .agg(
            songs=("song_name", "count"),
            total_words=("word_count", "sum"),
            mean_words_per_song=("word_count", "mean"),
        )
        .reset_index()
        .sort_values("total_words", ascending=False)
    )

    return album_counts


def plot_top_words(
    df,
    album=None,
    n=20,
    col="slategray",
    text_col="lyrics_clean",
    album_col="album",
    remove_stopwords=True,
    extra_stopwords=None,
    ax=None,
):
    """Plot the top words for all lyrics or one album."""
    import matplotlib.pyplot as plt

    counts = top_words(
        df,
        album=album,
        n=n,
        text_col=text_col,
        album_col=album_col,
        remove_stopwords=remove_stopwords,
        extra_stopwords=extra_stopwords,
    ).sort_values("count")

    if ax is None:
        _, ax = plt.subplots(figsize=(5, 3))

    ax.barh(counts["word"], counts["count"], color=col)

    if album is None:
        ax.set_title("Most Frequent Words in Ben Gibbard's Lyrics")
    else:
        ax.set_title(f"Most Frequent Words in the Album: {album}")

    ax.set_xlabel("Frequency")
    ax.set_ylabel("")

    return ax


def count_words(df, album=None, n=20, col="slategray"):
    """Backward-compatible wrapper for plotting top lyric words."""
    import matplotlib.pyplot as plt

    ax = plot_top_words(df, album=album, n=n, col=col)
    plt.show()
    return ax
