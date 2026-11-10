import logging
import sys

import pytest

import vcard2csv


def test_directory_without_vcards_exits_cleanly(tmp_path, capfd, caplog, monkeypatch):
    empty = tmp_path / "empty"
    empty.mkdir()
    out = tmp_path / "out.tsv"
    monkeypatch.setattr(sys, "argv", ["vcard2csv", str(empty), str(out)])
    with caplog.at_level(logging.ERROR, logger="vcard2csv"):
        with pytest.raises(SystemExit) as exc_info:
            vcard2csv.main()
    assert exc_info.value.code == 1
    assert "no files ending with" in caplog.text
    _, err = capfd.readouterr()
    assert "Traceback" not in err
