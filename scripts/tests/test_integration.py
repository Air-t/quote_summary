from ..utils import extract_from_ods


def test_extract_from_ods(temp_ods_file, tmp_path):
    log_file = tmp_path / "log.txt"

    est, total = extract_from_ods(temp_ods_file, str(log_file))

    assert est == "100"
    assert total == "50"
