#!/bin/bash
#SBATCH --nodes=1                       # number of nodes requested
#SBATCH --ntasks=1                      # number of tasks (default: 1)
#SBATCH --cpus-per-task=1               # number of CPUs per task
#SBATCH --partition=parallel            # partition to run in (serial or parallel)
#SBATCH --job-name=net                  # job name
#SBATCH --output=log/enz-%N-%j.out      # output file name
#SBATCH --error=log/enz-%N-%j.err       # error file name
#SBATCH --time=48:00:00                 # runtime requested
#SBATCH --mail-user=hkim78@asu.edu      # notification email
#SBATCH --mail-type=END,FAIL            # notification type
#SBATCH --export=ALL
#SBATCH --array 1-3

module purge
module load python/3.7.1

number=$((${SLURM_ARRAY_TASK_ID}-1))

# run the application:
python3 generating_enz_com_edge_lists_cluster.py  $number