import csv
import argparse

def filter_columns(input_file, output_file, columns_to_keep):
    with open(input_file, newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        filtered_columns = [col for col in columns_to_keep if col in reader.fieldnames]
        with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=filtered_columns)
            writer.writeheader()
            for row in reader:
                writer.writerow({col: row[col] for col in filtered_columns})

def main():
    fixed_colums=['Summary', 'Issue key', 'Status']
    parser = argparse.ArgumentParser(description='Filter specific columns from a Jira CSV export.')
    parser.add_argument('input_csv', help='Path to the input Jira CSV file')
    parser.add_argument('output_csv', help='Path to the output filtered CSV file')
    parser.add_argument('--columns', nargs='*', default=[],
                        help='List of columns to retain (default: Summary, Issue key, Status)')
    args = parser.parse_args()

    fixed_colums.extend(args.columns)

    filter_columns(args.input_csv, args.output_csv, fixed_colums)

if __name__ == '__main__':
    main()
