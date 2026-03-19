from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from sklearn.decomposition import PCA

import pandas as pd 

def decomp(df, vec):
    X = vec.transform(df["lyrics_clean"]) 
    X_dense = X.toarray()

    pca = PCA(n_components=2)
    X_2d = pca.fit_transform(X_dense)

    df_out = df.copy()

    df_out["x"] = X_2d[:, 0]
    df_out["y"] = X_2d[:,1]

    return df_out

def vectorize(text_col, index = None):
    """Take song column and make it into the numeric feature matrix
    """
    v = TfidfVectorizer(
        stop_words = "english",
        max_features = 5500 
        )

    X = v.fit_transform(text_col)

    v.get_feature_names_out()
    tfidf = pd.DataFrame(X.toarray(), 
                         columns = v.get_feature_names_out(),
                         index = index)

    return tfidf, v

def split(df):
    """split the data into train and test"""

    y = df["band_name"] # outcome variable
    X = df["lyrics_clean"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size = 0.2, shuffle = True, stratify = y)
    
    return X_train, X_test, y_train, y_test
