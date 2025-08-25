#!/bin/bash
#SBATCH --job-name=sub_processing_array      # Name of the job
#SBATCH --account=def-rmcintos               # Account
#SBATCH --time=00:5:00                       # Max runtime
#SBATCH --cpus-per-task=1                    # Number of CPUs per task
#SBATCH --mem=1G                             # Memory per task
#SBATCH --output=logs/sub_task_%A_%a.out     # Standard output log
#SBATCH --error=logs/sub_task_%A_%a.err      # Standard error log
#SBATCH --array=1-46                         # Number of tasks (one per subject)

# Each array task will use $SLURM_ARRAY_TASK_ID to pick a subject from the list
subject_list=($(cat /project/ctb-rmcintos/jwangbay/DO_NOT_USE_THIS_OR_jwangbay_OUTSIDE_OF_TRAINING/data-sets/BRS/present_subjects.tsv))
SUB="${subject_list[$((SLURM_ARRAY_TASK_ID-1))]}"

# Run Python script for this subject
python ~/scratch/BRS_Training/job_submission_scripts/2_process_one_subject.py "$SUB"
