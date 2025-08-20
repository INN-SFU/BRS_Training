"""
Script: generate_bdi_scores_CL.py

Description:
    This script computes total BDI scores for each subject and writes a subject-specific TSV file.
    It filters the dataset to include only subjects listed in a user-specified subject list file.
    Allows the user to specify the output directory for generated files.


Inputs:
    - BDI input TSV file
        e.g., /project/ctb-rmcintos/jwangbay/DO_NOT_USE_THIS_OR_jwangbay_OUTSIDE_OF_TRAINING/data-sets/BRS/assessments/desc-summary_date-20250721_bdigad.tsv
    - List of subject IDs (e.g., sub-BRS0034), one per line:
    - Output directory path for saving results


Outputs:
    - One TSV per subject in the specified output directory
      Format: <QID1>_bdi_score.tsv (e.g., BRS0034_bdi_score.tsv)
      Content: Two columns — QID1, BDI_score


Usage:
    python generate_bdi_scores_CL.py <bdi_input_tsv> <present_subs_tsv> <output_dir>


Example:
    python generate_bdi_scores_CL.py \
        /project/data/desc-summary_date-20250721_bdigad.tsv \
        ~/scratch/BRS_subset/present_subs.tsv \
        ~/scratch/BRS_subset/mood_outputs


Author: Leanne Rokos
Date: 13-08-2025
"""

import os
import pandas as pd
import sys

# === Check command-line arguments & set initial variables ===
if len(sys.argv) != 4:
    print("Usage: python generate_bdi_scores_CL.py <bdi_input_tsv> <present_subs_tsv> <output_dir>")
    sys.exit(1)

input_path = os.path.expanduser(sys.argv[1])
present_subjects_path = os.path.expanduser(sys.argv[2])
output_dir = os.path.expanduser(sys.argv[3])

subject_id_col = 'QID1'  # Column name for subject IDs

# === Create output directory if it doesn't exist ===
os.makedirs(output_dir, exist_ok=True)

# === Read the list of present subjects ===
print(f"Reading present subject list from: {present_subjects_path}")
try:
    with open(present_subjects_path, 'r') as f:
        present_subs = [line.strip() for line in f]
    print(f"Found {len(present_subs)} subject IDs in present_subjects.tsv")
except FileNotFoundError:
    raise FileNotFoundError(f"Could not find: {present_subjects_path}")

# === Load the full BDI dataset ===
print(f"Reading BDI data from: {input_path}")
try:
    bdigad_df = pd.read_csv(input_path, sep='\t')
except FileNotFoundError:
    raise FileNotFoundError(f"Could not find: {input_path}")

# === Check subject ID column exists ===
if subject_id_col not in bdigad_df.columns:
    raise ValueError(f"Subject ID column '{subject_id_col}' not found in input data.")

# === Drop the extra header rows and create a subID column ===
bdigad_df = bdigad_df.drop(bdigad_df.index[:2])
bdigad_df.loc[:,'subjectID'] = 'sub-' + bdigad_df['QID1'].astype(str) 

# === Filter only present subjects ===
print("Filtering to present subjects...")
matched_df = bdigad_df[bdigad_df['subjectID'].isin(present_subs)].copy()
print(f"Matched {len(matched_df)} subjects from the present_subjects list.")

# === Warn about unmatched subjects ===
present_ids = set(present_subs)
actual_ids = set(bdigad_df['subjectID'].astype(str))
unmatched = present_ids - actual_ids
if unmatched:
    print(f"Warning: {len(unmatched)} subject IDs in present_subjects.tsv were not found in the BDI data.")
    for uid in sorted(unmatched):
        print(f" - sub-{uid}")

# === Define function to compute total BDI score ===
def compute_bdi_score(df):
    bdi_items = df.filter(like='QBDI')
    if bdi_items.empty:
        raise ValueError("No columns found with prefix 'QBDI'. Check input data.")
    bdi_items = bdi_items.apply(pd.to_numeric, errors='coerce')
    df['BDI_score'] = bdi_items.sum(axis=1)
    return df

# === Compute BDI scores for filtered data ===
print("Computing BDI scores...")
mood_df = compute_bdi_score(matched_df)

# === Write one TSV per present subject ===
print(f"Saving individual BDI score files to: {output_dir}")
for idx, row in mood_df.iterrows():
    subj_id = row['subjectID']
    bdi_score = row['BDI_score']
    subj_df = pd.DataFrame({'subjectID': [subj_id], 'BDI_score': [bdi_score]})
    output_file = os.path.join(output_dir, f"{subj_id}_bdi_score.tsv")
    subj_df.to_csv(output_file, sep='\t', index=False)
    print(f"Saved: {output_file}")

print(f"\nFinished! BDI scores saved for {len(mood_df)} present subjects.")
