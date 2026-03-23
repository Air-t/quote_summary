import zipfile

import pytest


def create_test_ods(path, estimated="100", members="50"):
    content_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<office:document-content
 xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
 xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0"
 xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">

<table:table>
  {"".join(["<table:table-row/>" for _ in range(51)])}

  <table:table-row>
    <table:table-cell><text:p>TOTAL TIME ESTIMATED:</text:p></table:table-cell>
    <table:table-cell><text:p>{estimated}</text:p></table:table-cell>
  </table:table-row>

  {"".join(["<table:table-row/>" for _ in range(11)])}

  <table:table-row>
    <table:table-cell><text:p>Total steel members:</text:p></table:table-cell>
    <table:table-cell><text:p>{members}</text:p></table:table-cell>
  </table:table-row>

</table:table>
</office:document-content>
"""

    with zipfile.ZipFile(path, "w") as z:
        z.writestr("content.xml", content_xml)


@pytest.fixture
def temp_ods_file(tmp_path):
    file_path = tmp_path / "test.ods"
    create_test_ods(str(file_path))
    return str(file_path)
