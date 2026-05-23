from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.decomposition import TruncatedSVD

import pandas as pd 


def decomp(
    df,
    vec,
    text_col="lyrics_clean",
    n_components=2,
    random_state=67,
):
    """Add sparse-friendly 2D TF-IDF components to a dataframe."""
    X = vec.transform(df[text_col].fillna(""))

    svd = TruncatedSVD(n_components=n_components, random_state=random_state)
    X_2d = svd.fit_transform(X)

    df_out = df.copy()

    df_out["x"] = X_2d[:, 0]
    df_out["y"] = X_2d[:, 1]

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
