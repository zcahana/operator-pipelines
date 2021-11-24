from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from operatorcert import github
from requests import HTTPError, Response


def test_get_session_github_token(monkeypatch: Any) -> None:
    monkeypatch.setenv("GITHUB_TOKEN", "123")
    session = github._get_session()

    assert session.headers["Authorization"] == "Bearer 123"


def test_get_session_no_auth() -> None:
    github._get_session(auth_required=False)


def test_get_session_no_auth() -> None:
    with pytest.raises(Exception):
        github._get_session(auth_required=True)


@patch("operatorcert.github._get_session")
def test_post(mock_session: MagicMock) -> None:
    mock_session.return_value.post.return_value.json.return_value = {"key": "val"}
    resp = github.post("https://foo.com/v1/bar", {})

    assert resp == {"key": "val"}


@patch("operatorcert.github._get_session")
def test_post_with_error(mock_session: MagicMock) -> None:
    response = Response()
    response.status_code = 400
    mock_session.return_value.post.return_value.raise_for_status.side_effect = (
        HTTPError(response=response)
    )
    with pytest.raises(HTTPError):
        github.post("https://foo.com/v1/bar", {})