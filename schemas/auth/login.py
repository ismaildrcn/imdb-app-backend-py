from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    password: str

class UserCreate(UserBase):
    email: str
    password: str
    full_name: str
    birth_date: str | None = None
    gender: str | None = None
    

class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True


