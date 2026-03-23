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