import os
import pandas as pd
from tqdm import tqdm
# change the recreated log root
# if your directory is not consisted with README
ROOT = "GroupedLog"
OUTPUT = "MergedLog"


if __name__ == "__main__":
    if not os.path.exists(OUTPUT):
        os.makedirs(OUTPUT)
    timestamps = []
    num_requests = []
    sizes = []
    for file_name in tqdm(os.listdir(ROOT)):
        df = pd.read_csv(os.path.join(ROOT, file_name), names=["timestamp", "num_request", "size"])
        timestamps.extend(df["timestamp"].to_numpy())
        num_requests.extend(df["num_request"].to_numpy())
        sizes.extend(df["size"].to_numpy())
    df=pd.DataFrame.from_dict(data={"timestamp": timestamps, "num_request": num_requests, "size": sizes})
    # drop duplicated record especially at 22:00 each day
    df=df.drop_duplicates(subset=["timestamp"])
    df=df.sort_values(by="timestamp")
    df.to_csv(os.path.join(OUTPUT, "merged.csv"), index=False)
