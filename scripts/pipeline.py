import argparse

import pandas as pd

from scripts.clean import clean_lyrics, summary
from scripts.gen_plots import save_all_figures
from scripts.nat_lang import make_nlp_datasets
from src.paths import (
    CLEAN_DATA_PATH,
    CLUSTER_DATA_PATH,
    PLOTTING_DATA_PATH,
    RAW_DATA_PATH,
    FIGURES_DIR,
    save_data,
    DATA_DIR
)


def run_pipeline(
    raw_data_path=RAW_DATA_PATH,
    clean_data_path=CLEAN_DATA_PATH,
    cluster_data_path=CLUSTER_DATA_PATH,
    plotting_data_path=PLOTTING_DATA_PATH,
    cluster_components=25,
    make_plots=True,
):
    print(f"Reading raw data from {raw_data_path}")
    df_raw = pd.read_csv(raw_data_path)
    summary(df_raw, raw=True)

    df_clean = clean_lyrics(df_raw)
    save_data(df_clean, clean_data_path, output="parquet")
    summary(df_clean)

    df_cluster, df_vis, df_public = make_nlp_datasets(
        df_clean,
        cluster_components=cluster_components,
    )

    save_data(df_cluster, cluster_data_path, output="parquet")
    print(f"Data for clustering saved to {cluster_data_path}")

    save_data(df_vis, plotting_data_path, output="parquet")
    print(f"Data for rough visualizations saved to {plotting_data_path}")

    save_data(df_public, DATA_DIR / "data_wo_lyrics.csv", output="csv")
    print(f"Data for rough visualizations saved to {DATA_DIR}")

    if make_plots:
        plots_saved = save_all_figures(df_clean, df_vis)
        print(f"Saved {plots_saved} plots to {FIGURES_DIR}")


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Run the local data pipeline from an existing raw lyrics CSV to "
            "cleaned, sentiment-scored, SVD-transformed datasets."
        )
    )
    parser.add_argument(
        "--raw-data",
        default=RAW_DATA_PATH,
        type=str,
        help="Path to raw lyrics CSV created by scripts/pull.py.",
    )
    parser.add_argument(
        "--cluster-components",
        default=75,
        type=int,
        help="Number of SVD components to save for clustering.",
    )
    parser.add_argument(
        "--skip-plots",
        action="store_true",
        help="Skip figure generation.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    run_pipeline(
        raw_data_path=args.raw_data,
        cluster_components=args.cluster_components,
        make_plots=not args.skip_plots,
    )


if __name__ == "__main__":
    main()
