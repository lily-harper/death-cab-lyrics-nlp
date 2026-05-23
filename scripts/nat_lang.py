import pandas as pd 

from src.analysis import decomp, vectorize
from src.paths import CLEAN_DATA_PATH, TRANSFORMED_DATA_PATH, save_data


def main():
    df = pd.read_parquet(CLEAN_DATA_PATH)

if __name__ == "__main__":
    main()


