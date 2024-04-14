from pydantic import BaseModel

class EmailCheck(BaseModel):
    email: str