import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import TruncatedSVD

from src.analysis import vectorize
from src.paths import CLEAN_DATA_PATH, FIGURES_DIR


COMPONENT_OPTIONS = [2, 5, 10, 25, 50, 100, 150, 175]
COMPONENTS_FIGURE_PATH = FIGURES_DIR / "svd_components_elbow.png"


def component_variance(X, components=COMPONENT_OPTIONS, random_state=67):
    """Return cumulative explained variance for each SVD component count."""
    max_components = min(X.shape) - 1
    valid_components = [n for n in components if n <= max_components]

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


def main():
    df = pd.read_parquet(CLEAN_DATA_PATH)
    X, _ = vectorize(df["lyrics_clean"])

    component_df = component_variance(X)
    print(component_df.to_string(index=False))

    plot_component_elbow(component_df)


if __name__ == "__main__":
    main()
