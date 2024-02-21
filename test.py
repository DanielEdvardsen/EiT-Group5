import csv

filename = 'fMRI_Data/sub-001/func/sub-001_task-Test_run-01_events.tsv'

with open(filename, 'r') as file:
    reader = csv.reader(file, delimiter='\t')
    for row in reader:
        # Process each row of the TSV file
        print(row[0], row[2])