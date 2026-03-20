import os
import csv
import zipfile
import xml.etree.ElementTree as ET

INPUT_DIR = input("Enter input directory: ").strip()
OUTPUT_DIR = input("Enter output directory: ").strip()

SUMMARY_FILE = os.path.join(OUTPUT_DIR, "summary.csv")
LOG_FILE = os.path.join(OUTPUT_DIR, "log.txt")

os.makedirs(OUTPUT_DIR, exist_ok=True)

def log_error(message):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(message + "\n")


def extract_from_ods(file_path):
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            with z.open('content.xml') as f:
                tree = ET.parse(f)
                root = tree.getroot()

        ns = {
            'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
            'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'
        }

        rows = root.findall(".//table:table-row", ns)

        total_estimated = None
        total_members = None

        for row_idx, row in enumerate(rows):
            cells = row.findall("table:table-cell", ns)

            values = []
            for cell in cells:
                texts = cell.findall(".//text:p", ns)
                cell_text = "".join([t.text or "" for t in texts]).strip()
                values.append(cell_text)

            # ---- Rule 1: TOTAL TIME ESTIMATED ----
            if "TOTAL TIME ESTIMATED:" in values:
                idx = values.index("TOTAL TIME ESTIMATED:")
                if idx + 1 < len(values):
                    total_estimated = values[idx + 1]

            # ---- Rule 2: Total steel members ----
            if "Total steel members:" in values:
                idx = values.index("Total steel members:")
                if idx + 1 < len(values):
                    total_members = values[idx + 1]

        return total_estimated, total_members

    except Exception as e:
        log_error(f"{file_path} -> ERROR: {str(e)}")
        return None, None


def process_directory():
    results = []

    for root_dir, _, files in os.walk(INPUT_DIR):
        for file in files:
            if file.lower().endswith(".ods"):
                full_path = os.path.join(root_dir, file)

                est, total = extract_from_ods(full_path)

                if est is None and total is None:
                    log_error(f"{full_path} -> No data found")
                else:
                    results.append([full_path, est, total])

    return results


def save_csv(data):
    with open(SUMMARY_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["File path", "Total members estimated", "Total members"])
        writer.writerows(data)


if __name__ == "__main__":
    data = process_directory()
    save_csv(data)

    print(f"\nDone!")
    print(f"Summary: {SUMMARY_FILE}")
    print(f"Errors: {LOG_FILE}")