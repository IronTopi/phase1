"""Minimalist authentication to be used by FastAPI"""

import os
import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()


##########
# "Security"
def validateCredentials (credentials: HTTPBasicCredentials = Depends(security)):
    """Validates the provided BasicAuth-credentials.
    Can be used on any FastAPI-route via Depends.

    Args:
        credentials (HTTPBasicCredentials, optional): BasicAuth credentials. Defaults to Depends(security) (handeled by FastPI-magic).

    Raises:
        HTTPException: 401 unauthorized, raised if credentials are not valid

    Returns:
        bool: True, if credentials are valid
    """
    # Encode the credentials to compare
    inputUsername = credentials.username.encode("utf-8")
    inputPassword = credentials.password.encode("utf-8")

    # Careless plaintext
    storedUsername = os.environ["API_USER"].encode ("utf-8")
    storedPassword = os.environ["API_PASSWORD"].encode ("utf-8")

    usernameOK = secrets.compare_digest(inputUsername, storedUsername)
    passwordOK = secrets.compare_digest(inputPassword, storedPassword)

    if usernameOK and passwordOK:
        return True

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid credentials",
                        headers={"WWW-Authenticate": "Basic"})