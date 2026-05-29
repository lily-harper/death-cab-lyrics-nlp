from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.decomposition import TruncatedSVD

from nltk.sentiment.vader import SentimentIntensityAnalyzer 

import pandas as pd 


def decomp(
    df,
    vec,
    text_col="lyrics_no_stopwords",
    n_components=2,
    random_state=67,
    component_prefix="svd",
):
    """Add sparse-friendly TF-IDF SVD components to a dataframe."""
    X = vec.transform(df[text_col].fillna(""))

    svd = TruncatedSVD(n_components=n_components, random_state=random_state)
    X_decomp = svd.fit_transform(X)

    df_out = df.copy()

    component_cols = [
        f"{component_prefix}_{i + 1}" for i in range(X_decomp.shape[1])
    ]
    components = pd.DataFrame(
        X_decomp,
        columns=component_cols,
        index=df_out.index,
    )

    df_out = pd.concat([df_out, components], axis=1)

    if n_components == 2:
        df_out["x"] = df_out[f"{component_prefix}_1"]
        df_out["y"] = df_out[f"{component_prefix}_2"]

    return df_out


def vectorize(
    text_col,
    index=None,
    stop_words="english",
    max_features=5500,
    return_df=False,
):
    """Fit TF-IDF and return a sparse feature matrix plus the vectorizer."""
    vectorizer = TfidfVectorizer(
        stop_words=stop_words,
        max_features=max_features,
    )

    X = vectorizer.fit_transform(text_col.fillna(""))

    if return_df:
        tfidf = pd.DataFrame.sparse.from_spmatrix(
            X,
            columns=vectorizer.get_feature_names_out(),
            index=index,
        )
        return tfidf, vectorizer

    return X, vectorizer


def vader(df, text_col="lyrics_clean"): 
    """Add VADER compound sentiment scores for a text column."""
    df = df.copy()
    analyzer = SentimentIntensityAnalyzer()

    df["sentiment"] = df[text_col].fillna("").apply(
        lambda x: analyzer.polarity_scores(x)["compound"]
    )

    return df 


def split(
    df,
    text_col="lyrics_clean",
    target_col="band_name",
    test_size=0.2,
    random_state=67,
):
    """Split text and target columns into train and test sets."""
    y = df[target_col]
    X = df[text_col].fillna("")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        shuffle=True,
        stratify=y,
        random_state=random_state,
    )
    
    return X_train, X_test, y_train, y_test
