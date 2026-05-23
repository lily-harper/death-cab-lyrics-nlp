from pathlib import Path
import pandas as pd

def find_project_root(start: Path) -> Path:
    start = start.resolve()

    if start.is_file():
        start = start.parent

    for parent in [start, *start.parents]:
        has_project_dirs = (parent / "data").is_dir() and (parent / "src").is_dir()
        has_project_files = (parent / "README.md").is_file() and (
            parent / "requirements.txt"
        ).is_file()
        is_git_repo = (parent / ".git").exists()

        if has_project_dirs and (is_git_repo or has_project_files):
            return parent

    raise FileNotFoundError(
        "Could not find project root. Expected a repo with data/, src/, "
        "and either .git/ or README.md plus requirements.txt."
    )

def save_data(df: pd.DataFrame, path, output):
    
    path = Path(path)

    path.parent.mkdir(parents=True, exist_ok= True)

    if output == "csv":
        df.to_csv(path, index = False)
    elif output == "parquet":
        df.to_parquet(path, index=False)
    else:
        raise ValueError("output must be 'csv' or 'parquet'")

    print(f"\n Saved dataset in {path}.")
    print(df.shape)

PROJECT_ROOT = find_project_root(Path(__file__).resolve())

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
CLEAN_DIR = DATA_DIR / "clean"

REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

RAW_DATA_PATH = RAW_DATA_DIR / "raw_scrape.csv"
CLEAN_DATA_PATH = CLEAN_DIR / "clean_lyrics.parquet" 
TRANSFORMED_DATA_PATH = CLEAN_DIR / "transformed_lyrics.parquet"

