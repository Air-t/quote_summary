from xml.etree.ElementTree import Element

from ..utils import get_cell_text_in_row, get_row_by_index


def test_get_row_by_index_simple():
    rows = [Element("row") for _ in range(5)]
    assert get_row_by_index(rows, 2) == rows[2]


def test_get_row_by_index_out_of_range():
    rows = [Element("row") for _ in range(3)]
    assert get_row_by_index(rows, 10) is None


def test_get_cell_text_in_row_basic():
    from xml.etree.ElementTree import fromstring

    xml = """
    <table:table-row xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0"
                     xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">
        <table:table-cell><text:p>A</text:p></table:table-cell>
        <table:table-cell><text:p>TOTAL TIME ESTIMATED:</text:p></table:table-cell>
        <table:table-cell><text:p>123</text:p></table:table-cell>
    </table:table-row>
    """

    row = fromstring(xml)

    result = get_cell_text_in_row(
        row,
        {
            "table": "urn:oasis:names:tc:opendocument:xmlns:table:1.0",
            "text": "urn:oasis:names:tc:opendocument:xmlns:text:1.0",
        },
        "TOTAL TIME ESTIMATED:",
    )

    assert result == "123"
