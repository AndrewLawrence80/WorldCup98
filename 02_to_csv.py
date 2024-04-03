import os
import re
import pandas as pd
from datetime import datetime
from collections import namedtuple
from typing import List
from tqdm import tqdm

# change the recreated log root
# if your directory is not consisted with README
ROOT = "RecreatedLog"
OUTPUT = "CSVLog"

Request = namedtuple('Request', ["timestamp", "size"])


def parse_log(log_path: str) -> List[Request]:
    request_list = []
    with open(log_path, 'r', encoding='ISO-8859-1') as file_handle:
        for line in file_handle.readlines():
            # split line, get time and size token
            tokens = re.split('\s+', line)
            time_token = tokens[3][1:]
            size_token = tokens[-2]
            # process time token
            timestamp = datetime.strptime(time_token, "%d/%b/%Y:%H:%M:%S")
            size = 1 if size_token == "-" or size_token == "0" else int(size_token)
            request_list.append(Request(timestamp, size))
    return request_list


if __name__ == "__main__":
    if not os.path.exists(OUTPUT):
        os.makedirs(OUTPUT)
    for file_name in tqdm(os.listdir(ROOT)):
        request_list = parse_log(os.path.join(ROOT, file_name))
        if len(request_list) == 0:
            continue
        else:
            request_list = Request(*zip(*request_list))
            df = pd.DataFrame.from_dict(data={"time": pd.to_datetime(request_list.timestamp), "size": request_list.size})
            df.to_csv(os.path.join(OUTPUT, file_name.split(".")[0]+".csv"), header=False, index=False)
