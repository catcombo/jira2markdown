"""Tests for the jira2markdown command-line interface."""

import io
import sys

import pytest

from jira2markdown.cli import main


class _TtyStdin(io.StringIO):
    """A stdin stub that claims to be a TTY so main() parses argv."""

    def isatty(self):
        return True


def _run_tty(monkeypatch, argv):
    monkeypatch.setattr(sys, "stdin", _TtyStdin(""))
    monkeypatch.setattr(sys, "argv", ["jira2markdown", *argv])


def test_cli_converts_text_argument(monkeypatch, capsys):
    _run_tty(monkeypatch, ["*bold*"])
    main()
    assert capsys.readouterr().out == "**bold**"


def test_cli_converts_file(monkeypatch, tmp_path, capsys):
    src = tmp_path / "in.txt"
    src.write_text("*bold*", encoding="utf-8")
    _run_tty(monkeypatch, ["-f", str(src)])
    main()
    assert capsys.readouterr().out == "**bold**"


def test_cli_missing_file_reports_error(monkeypatch, tmp_path, capsys):
    missing = tmp_path / "does-not-exist.txt"
    _run_tty(monkeypatch, ["-f", str(missing)])
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 2
    captured = capsys.readouterr()
    assert "does-not-exist.txt" in captured.err
    assert "Traceback" not in captured.err
    assert captured.out == ""
