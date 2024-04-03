import os
import pandas as pd
from tqdm import tqdm
from collections import namedtuple
from typing import List
# change the csv log root
# if your directory is not consisted with README
ROOT = "CSVLog"
OUTPUT = "GroupedLog"

Request = namedtuple("Request", ["timestamp", "num_request", "size"])


def read_and_group(csv_path: str, out_dir: str) -> pd.DataFrame:
    
    df = pd.read_csv(csv_path, names=["timestamp", "size"], parse_dates=["timestamp"])
    timestamps = df["timestamp"].to_numpy()
    sizes = df["size"].to_numpy()

    # do not use df.groupby because the algorithm complexity is O(n^2), which is really slow
    # use the follwing algorithm optimized with comlexity O(n)
    requests: List[Request] = []
    # current procssing minute
    current_minute = timestamps[0].astype("datetime64[m]")
    minute_request = 0
    minute_size = 0
    for idx in range(len(timestamps)):
        t_minute = timestamps[idx].astype("datetime64[m]")
        if current_minute != t_minute: # the next minute is coming
            requests.append(Request(current_minute, minute_request, minute_size))
            minute_request = 0
            minute_size = 0
            current_minute = t_minute
        minute_request += 1
        minute_size += sizes[idx]
    # don't forget the last minute
    requests.append(Request(current_minute, minute_request, minute_size))
    requests = Request(*zip(*requests))
    pd.DataFrame.from_dict(data={"timestamp": requests.timestamp, "num_request": requests.num_request, "size": requests.size}).to_csv(os.path.join(out_dir, csv_path.split(os.path.sep)[-1]), header=False, index=False)


if __name__ == "__main__":
    if not os.path.exists(OUTPUT):
        os.makedirs(OUTPUT)
    for file_name in tqdm(os.listdir(ROOT)):
        read_and_group(os.path.join(ROOT, file_name), OUTPUT)
