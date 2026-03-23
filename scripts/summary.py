import os

from .utils import process_directory, save_csv

if __name__ == "__main__":
    INPUT_DIR = input("Enter input directory: ").strip()
    OUTPUT_DIR = input("Enter output directory: ").strip()
    SUMMARY_FILE = os.path.join(OUTPUT_DIR, "summary.csv")
    LOG_FILE = os.path.join(OUTPUT_DIR, "log.txt")

    data = process_directory(INPUT_DIR, LOG_FILE)
    save_csv(data, SUMMARY_FILE)

    print("\nDone!")
    print(f"Summary: {SUMMARY_FILE}")
    print(f"Errors: {LOG_FILE}")
