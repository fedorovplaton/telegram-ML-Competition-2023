import pandas as pd


if __name__ == "__main__":
    df = pd.read_parquet("../../data/processed/bigcode-the-stack.parquet")

    print(df.columns)
    print(df["tglang"].unique())
    print(df[""])


