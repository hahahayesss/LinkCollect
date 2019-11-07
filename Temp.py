import numpy as np
import pandas as pd

raw_data = pd.read_csv("jobs.csv")
time = np.zeros(raw_data.shape)
collected = np.zeros(raw_data.shape)
file_name = np.zeros(raw_data.shape)

raw_data["time"] = time
raw_data["collected"] = collected
raw_data["file_name"] = file_name

raw_data = raw_data.astype({"time": "int64",
                            "collected": "int64",
                            "file_name": "int64"})

raw_data.to_csv("_jobs.csv")
