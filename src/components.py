"""Optional diagnostic plot for choosing an SVD component count."""

import argparse

import pandas as pd
from sklearn.decomposition import TruncatedSVD

from src.analysis import vectorize
from src.paths import CLEAN_DATA_PATH, FIGURES_DIR


COMPONENT_OPTIONS = [2, 5, 10, 25, 50, 100, 150, 175]
COMPONENTS_FIGURE_PATH = FIGURES_DIR / "diagnostics" / "svd_components_elbow.png"


def component_variance(X, components=COMPONENT_OPTIONS, random_state=67):
    """Return cumulative explained variance for each SVD component count."""
    max_components = min(X.shape) - 1
    valid_components = [n for n in components if n <= max_components]

    if not valid_components:
        raise ValueError(
            "No valid component counts. Component counts must be less than "
            f"min(X.shape), which is {min(X.shape)} for this matrix."
        )

    explained = []
    for n_components in valid_components:
        svd = TruncatedSVD(n_components=n_components, random_state=random_state)
        svd.fit(X)
        explained.append(svd.explained_variance_ratio_.sum())

    return pd.DataFrame(
        {
            "components": valid_components,
            "explained_variance": explained,
        }
    )


def plot_component_elbow(component_df, output_path=COMPONENTS_FIGURE_PATH):
    """Save an elbow plot of SVD components versus explained variance."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(
        component_df["components"],
        component_df["explained_variance"],
        marker="x",
    )
    ax.set_xlabel("Number of SVD components")
    ax.set_ylabel("Cumulative explained variance")
    ax.set_title("Explained Variance by SVD Components")
    ax.grid(alpha=0.25)

    fig.tight_layout()
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved {output_path}")


def save_component_elbow(
    clean_data_path=CLEAN_DATA_PATH,
    output_path=COMPONENTS_FIGURE_PATH,
    components=COMPONENT_OPTIONS,
    text_col="lyrics_clean",
):
    """Create the optional SVD component diagnostic plot from cleaned data."""
    df = pd.read_parquet(clean_data_path)
    X, _ = vectorize(df[text_col])

    component_df = component_variance(X, components=components)
    print(component_df.to_string(index=False))

    plot_component_elbow(component_df, output_path=output_path)

    return component_df


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Generate an optional SVD component elbow plot from the cleaned "
            "lyrics dataset."
        )
    )
    parser.add_argument(
        "--input",
        default=CLEAN_DATA_PATH,
        type=str,
        help="Path to the cleaned parquet dataset.",
    )
    parser.add_argument(
        "--output",
        default=COMPONENTS_FIGURE_PATH,
        type=str,
        help="Path where the component elbow plot should be saved.",
    )
    parser.add_argument(
        "--components",
        default=COMPONENT_OPTIONS,
        nargs="+",
        type=int,
        help="SVD component counts to evaluate.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    save_component_elbow(
        clean_data_path=args.input,
        output_path=args.output,
        components=args.components,
    )


if __name__ == "__main__":
    main()
