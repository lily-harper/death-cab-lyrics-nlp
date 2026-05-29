import pandas as pd 

from src.analysis import decomp, vectorize, vader
from src.paths import CLEAN_DATA_PATH, CLUSTER_DATA_PATH, PLOTTING_DATA_PATH, save_data, DATA_DIR


def make_nlp_datasets(df: pd.DataFrame, cluster_components=25):
    df = vader(df)
    X, vectorizer = vectorize(df["lyrics_no_stopwords"])

    drop = ["genius_url", "song_name_clean"]
    
    df = df.drop(columns=drop, errors="ignore")

    print(f"The TF-IDF matrix was {X.shape[0]} by {X.shape[1]}")

    df_cluster = decomp(df, vectorizer, n_components=cluster_components)
    df_vis = decomp(df, vectorizer, n_components=2)

    df_public = df_cluster.drop(columns = ["lyrics_no_stopwords", "lyrics_clean"])

    return df_cluster, df_vis, df_public


def main():
    df = pd.read_parquet(CLEAN_DATA_PATH)
    df_cluster, df_vis, df_public = make_nlp_datasets(df)

    save_data(df_cluster, CLUSTER_DATA_PATH, output="parquet")
    print(f"Data for clustering saved to {CLUSTER_DATA_PATH}")
    print(f"Rows: {df_cluster.shape[0]}")
    print(f"Columns: {df_cluster.shape[1]}")
    print("\n")

    save_data(df_vis, PLOTTING_DATA_PATH, output="parquet")
    print(f"Data for rough visualizations saved to {PLOTTING_DATA_PATH}")
    print(f"Rows: {df_vis.shape[0]}")
    print(f"Columns: {df_vis.shape[1]}")

    save_data(df_public, DATA_DIR / "data_wo_lyrics.csv", output="csv")

if __name__ == "__main__":
    main()
