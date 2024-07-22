import csv

# Define the input and output file names
input_file = 'Webhooklogs_2024_07_22.csv'
output_file = 'error_logs.csv'

# Open the input CSV file
with open(input_file, mode='r', newline='') as infile:
    reader = csv.DictReader(infile)
    
    # Open the output CSV file
    with open(output_file, mode='w', newline='') as outfile:
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        
        # Write the header row to the output file
        writer.writeheader()
        
        # Iterate through each row in the input file
        for row in reader:
            # Check if the Result column contains "Error"
            if "Error" in row['Result']:
                # Write the row to the output file
                writer.writerow(row)

print(f'Filtered rows with errors have been written to {output_file}')
