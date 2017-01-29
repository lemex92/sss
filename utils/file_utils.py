import csv


def read_rows_from_csv(file_path, delim=",", quote_char="|"):
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=delim, quotechar=quote_char)
        return [row for row in reader]

