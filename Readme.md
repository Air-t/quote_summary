# Quote Summary Tool

This repository provides a simple way to collect and summarize data from multiple quote files (`quote.ods`) stored across folders. It generates a `summary.csv` file containing the extracted information.

## 📌 Purpose

The goal of this project is to automate the process of collecting data from multiple quote files (`quote.ods`) located in a directory and its subdirectories, and compile them into a single summary file (`summary.csv`).

---

## 🚀 Getting Started

### 1. Clone or Fork the Repository

```bash
git clone https://github.com/Air-t/quote_summary.git
cd quote_summary
```

---

## ▶️ How to Run

There are three ways to run the tool depending on your setup:

---

### ✅ Option 1: Run using Windows Executable Script

You can run the preconfigured batch file by clicking on it:

```bash
summary.bat
```

- This will launch the script in a Windows command prompt.
- You will be prompted to:
  - Enter the **source folder** (where quote files are located)
  - Enter the **output folder** (where `summary.csv` will be saved)

---

### ✅ Option 2: Run using Python Module

From the root directory of the project, run:

```bash
python -m scripts.summary
```

- The script will prompt you for:
  - The **source folder** (it will recursively search subfolders)
  - The **output folder** for the generated `summary.csv`

---

### ✅ Option 3: Run with SDS2 Detailing Software (Recommended)

If you are using SDS2 detailing software,
you can run script by SDS2 parametric run
(python 3 support - SDS2 2025 and higher):

```bash
sds2_quote_summary_python3.py
```

- The script will prompt you to:
  - Select the **starting folder** for data collection
  - Choose where to save the `summary.csv`

---

## 📂 How It Works

- The script scans the selected **source directory**
- It recursively searches all subfolders
- It looks for files named:

```
<quote_name>.ods
```

- Extracts relevant data from each file
  - looks for row 52 with text "TOTAL TIME ESTIMATED:" - returns number of total members estimated
  - looks for row 64 with text "Total steel members:" - returns number of total members
- Compiles everything into:

```
summary.csv
```

---

## 📄 Output

- A single CSV file:
  - `summary.csv`

- Contains aggregated data from all discovered quote files

---

## ⚙️ Requirements

- Python 3.10
- Script uses python native packages so there is no need to install requirements,
  however it also includes SDS2 GUI when run with method 3. This packages has fallback to python input if not present.
  Packages included in requirements.txt are for testing purpose only:

```bash
pip install -r requirements.txt
```

---

## 🧩 Notes

- Ensure all quote files follow the expected format (`quote.ods`)
- The script assumes consistent structure across files for accurate extraction
- Works best when directory structure is organized and predictable

---

## 🤝 Contributing

Feel free to fork the repository and submit pull requests to improve functionality or add features.

---
