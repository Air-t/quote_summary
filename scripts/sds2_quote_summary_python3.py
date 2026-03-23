# SDS2 with python 3.10 support script.
# Run directly from SDS2 interface.

import os
import csv
import zipfile
import xml.etree.ElementTree as ET


# Folder prefixes that will not be searched
SKIP_PREFIXES = ("_", "@Recently-Snapshot")

# Name space for xml file processing
NS = {
    'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
    'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'
}

# Search text for xml required fields
TOTAL_MEMBERS_ESTIMATED_TEXT = "TOTAL TIME ESTIMATED:"
TOTAL_MEMBERS_TEXT = "Total steel members:"

# CSV output utils
SUMMARY_OUTPUT_COLUMN_NAMES = [
    "File path", "Total members estimated", "Total members"
]


def log_error(message, log_file):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(message + "\n")

def get_row_by_index(rows, target_index):
    current_index = 0

    for row in rows:
        repeat = int(row.attrib.get(
            '{urn:oasis:names:tc:opendocument:xmlns:table:1.0}number-rows-repeated',
            1
        ))

        for _ in range(repeat):
            if current_index == target_index:
                return row
            current_index += 1

    return None

def get_cell_text_in_row(row, ns, search_text, index_increment=1):
    cells = row.findall("table:table-cell", ns)
    values = []
    for cell in cells:
        texts = cell.findall(".//text:p", ns)
        cell_text = "".join([t.text or "" for t in texts]).strip()
        values.append(cell_text)

    if search_text in values:
        idx = values.index(search_text)
        if idx + 1 < len(values):
            return values[idx + index_increment]
    return None


def extract_from_ods(file_path, log_file):
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            with z.open('content.xml') as f:
                tree = ET.parse(f)
                root = tree.getroot()

        rows = root.findall(".//table:table-row", NS)
        total_estimated = get_cell_text_in_row(
            get_row_by_index(rows, 51), NS,TOTAL_MEMBERS_ESTIMATED_TEXT
        )
        total_members = get_cell_text_in_row(
            get_row_by_index(rows, 63), NS, TOTAL_MEMBERS_TEXT
        )

        return total_estimated, total_members

    except Exception as e:
        log_error(f"{file_path} -> ERROR: {str(e)}", log_file)
        return None, None

def process_directory(input_dir, log_file):
    results = []

    for root_dir, dirs, files in os.walk(input_dir):
        dirs[:] = [d for d in dirs if not d.startswith(SKIP_PREFIXES)]
        for file in files:
            if file.lower().endswith(".ods"):
                full_path = os.path.join(root_dir, file)
                est, total = extract_from_ods(full_path, log_file)
                if est is None and total is None:
                    log_error(f"{full_path} -> No data found", log_file)
                else:
                    results.append([full_path, est, total])

    return results

def save_csv(data, summary_file):
    with open(summary_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(SUMMARY_OUTPUT_COLUMN_NAMES)
        writer.writerows(data)


if __name__ == "__main__":
    INPUT_DIR = input("Enter input directory: ").strip()
    OUTPUT_DIR = input("Enter output directory: ").strip()
    SUMMARY_FILE = os.path.join(OUTPUT_DIR, "summary.csv")
    LOG_FILE = os.path.join(OUTPUT_DIR, "log.txt")

    data = process_directory(INPUT_DIR, LOG_FILE)
    save_csv(data, SUMMARY_FILE)

    print(f"\nDone!")
    print(f"Summary: {SUMMARY_FILE}")
    print(f"Errors: {LOG_FILE}")