from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    id: int
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    gender: Optional[int | str] = None
    birthdate: Optional[str] = None