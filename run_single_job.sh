#!/bin/bash
#SBATCH --job-name=sub_processing        # Name of the job
#SBATCH --account=def-rmcintos           # Account
#SBATCH --time=00:10:00                  # Max runtime (HH:MM:SS)
#SBATCH --cpus-per-task=1                # Number of CPU cores per task
#SBATCH --mem=1G                         # Memory per task
#SBATCH --output=logs/sub_task_%j.out    # File for standard output (%j = job ID)

# Load required modules
module load scipy-stack

# Run the Python script
python ~/scratch/BRS_Training_Dev/process_all_subjects.py # TO DO: CHANGE BACK TO BRS_TRAINING
