#!/usr/bin/env python3
import pandas as pd
import time
import os

# Path to TSV with subjects
subject_list_path = os.path.expanduser("~/scratch/BRS_subset/present_subjects.tsv")

# Load subjects
subs = pd.read_csv(subject_list_path, header=None)[0].tolist()

for sub in subs:
    print(f"Processing subject: {sub}")
    time.sleep(2)  # placeholder for actual processing
    print(f"Finished subject: {sub}")

print("All subjects processed!")
