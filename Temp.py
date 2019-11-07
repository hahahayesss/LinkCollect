import numpy as np
import pandas as pd

raw_list = pd.read_csv("_jobs.csv").values
total = 0
for data in raw_list:
    total += data[3]

print("Total:", total)
