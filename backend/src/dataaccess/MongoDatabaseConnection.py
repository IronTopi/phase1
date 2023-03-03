from pydantic import BaseModel
from dataaccess.IDatabaseConnection import IDatabaseConnection

class MongoDatabaseConnection (IDatabaseConnection):


class MongoConnectionConfig (BaseModel):
    IP: str
    Port: int
    User: str
    Password: str

    Database: str
    Collection: str