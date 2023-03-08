import os
import pytest

from fastapi import HTTPException
from fastapi.security.http import HTTPBasicCredentials
from auth import validateCredentials


def test_LoginSuccess():
    storedUsername = os.environ["API_USER"].encode("utf-8")
    storedPassword = os.environ["API_PASSWORD"].encode("utf-8")
    validCredentials = HTTPBasicCredentials(username=storedUsername, password=storedPassword)

    assert validateCredentials(validCredentials)


def test_LoginFailure():
    storedUsername = (os.environ["API_USER"] + "nope").encode("utf-8")
    storedPassword = (os.environ["API_PASSWORD"] + "nope").encode("utf-8")
    validCredentials = HTTPBasicCredentials(username=storedUsername, password=storedPassword)

    with pytest.raises(HTTPException) as e_info:
        validateCredentials(validCredentials)
