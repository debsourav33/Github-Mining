from typing import List
import os
import csv


def save_as_csv(file_path, data: List[str], mode="a", header=""):
    write_header = False
    if not os.path.exists(file_path):
        write_header = True

    with open(file_path, mode=mode) as file:
        csv_writer = csv.writer(file)
        if write_header:
            csv_writer.writerow(header)
        csv_writer.writerow(data)
