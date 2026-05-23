import pandas as pd 

from src.analysis import decomp, vectorize, vader
from src.paths import CLEAN_DATA_PATH, CLUSTER_DATA_PATH, PLOTTING_DATA_PATH, save_data


def make_nlp_datasets(df: pd.DataFrame, cluster_components=75):
    df = vader(df)
    X, vectorizer = vectorize(df["lyrics_clean"])

    drop = ["genius_url", "lyrics", "song_name_clean"]
    
    df = df.drop(columns=drop, errors="ignore")

    print(f"The TF-IDF matrix was {X.shape[0]} by {X.shape[1]}")

    df_cluster = decomp(df, vectorizer, n_components=cluster_components)
    df_vis = decomp(df, vectorizer, n_components=2)

    return df_cluster, df_vis


def main():
    df = pd.read_parquet(CLEAN_DATA_PATH)
    df_cluster, df_vis = make_nlp_datasets(df)

    save_data(df_cluster, CLUSTER_DATA_PATH, output="parquet")
    print(f"Data for clustering saved to {CLUSTER_DATA_PATH}")

    save_data(df_vis, PLOTTING_DATA_PATH, output="parquet")
    print(f"Data for rough visualizations saved to {PLOTTING_DATA_PATH}")

if __name__ == "__main__":
    main()
