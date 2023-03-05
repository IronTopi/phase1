import os
import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()


##########
# "Security"
def validateCredentials (credentials: HTTPBasicCredentials = Depends(security)):
    # Encode the credentials to compare
    inputUsername = credentials.username.encode("utf-8")
    inputPassword = credentials.password.encode("utf-8")

    # Careless plaintext
    storedUsername = os.environ["API_USER"].encode ("utf-8")
    storedPassword = os.environ["API_PASSWORD"].encode ("utf-8")

    usernameOK = secrets.compare_digest(inputUsername, storedUsername)
    passwordOK = secrets.compare_digest(inputPassword, storedPassword)

    if usernameOK and passwordOK:
        return credentials

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid credentials",
                        headers={"WWW-Authenticate": "Basic"})