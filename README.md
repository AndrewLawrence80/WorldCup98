# WorldCup98 Dataset - Download and Processing

> **Note**: It takes a long time to rebuild nginx log and transfer it into csv format. I provide proceeding results after step [Group Request by Minute](#group-request-by-minute) in the repo. Feel free to use them.

## Download the Dataset

The original dataset description is available at <https://ita.ee.lbl.gov/html/contrib/WorldCup.html>. The dataset is archived on an FTP server, which may not be supported for direct downloading using modern browsers like Chrome and Firefox. A practical way is to use dedicated download tools like [wget](https://www.gnu.org/software/wget/) or [FileZilla](https://filezilla-project.org/).

```bash
wget -r ftp://ita.ee.lbl.gov/traces/WorldCup/
```

You should reorganize the download directory by following these steps:

- Remove the WorldCup.html
- Unzip the WorldCup_tools.tar.gz to an independent directory
- Place all the wc_day*.gz data files in an independent directory

Now the directory tree should look like this:

- ita_public_tools
  - bin
  - ...
- WorldCup
  - wc_day1_1.gz
  - wc_day2_1.gz
  - ...
  - wc_day92_1.gz

## Build the Tool

```bash
cd ita_public_tools && make
```

## Rebuild the Nginx log

Run `01_rebuild.py`, the `.py` file will call the built tool to rebuld Nginx log from `.gz` format.
Check `Tools` section in the [description page](https://ita.ee.lbl.gov/html/contrib/WorldCup.html) for more details.
Default output directory is `RecreatedLog`.

## Transfer Log to CSV

Run `02_to_csv.py`, the `.py` file will transfer the rebuilt Nginx log in to CSV format.
Each row consists of data like `1998-04-30 21:30:17,24736`, representing timestamp, transferred data size.
Every record in Niginx log whose request size is '-' is replaced by 1.
Default input directory is `RecreatedLog`.
Default output directory is `CSVLog`.

## Group Request by Minute

Run `03_group_request_by_min.py`, the `.py` file will further group the Nginx log into pre-minute record.
Each row consists of data like `1998-05-04 22:00:00,543,4234845`, representing per-minute timestamp, request number,transferred data size.
Default input directory is `CSVLog`.
Default output directory is `GroupedLog`.

## Merge Grouped Request

Run `04_merge.py`, the `.py` file will merge the grouped requests.
Default input directory is `GroupedLog`.
Default output directory is `MergedLog`.

> **Note:** The original data processing is done. Further steps will remove anomalies and smooth the data.
> You can stick to merged data in `MergedLog` if you prefer to shuffle data by your self.

## Remove Anomalies

Run `05_remove_anomaly.ipynb`, the `.ipynb` notebook will smooth the request number.
The notebook find anomalies and smooth values as following:

1. Calculate the absolute value of the first order difference of the request number.
2. Sort the absolute values in descending order and plot the values.
3. Large, anomalous absolute values take a small portion of the whole absolute value set. The figure will have an obvious "elbow".
4. Take the elbow value as criteria, remove the sudden peaks and valleys in the figure of the original request number.
Default input directory is `MergedLog`.
Default output directory is `AnomalyRemovedLog`.

## Fine Tune the Dataset Manually

There are still some anomalies after smoothing, requiring further fine tune, especially at timestamp 22:00 each day.
Manually tagged anomaly index are in `FineTunedLog/anomaly_index.json`. You can edit it freely if you find more anomalies.
Run `06_fine_tune.ipynb`, the `.ipynb` notebook will further fine-tune the smoothed data.
Default input directory is `AnomalyRemovedLog`.
Default output directory is `FineTunedLog`.
