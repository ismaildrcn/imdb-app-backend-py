from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    password: str

class UserCreate(UserBase):
    email: str
    password: str
    full_name: str
    

class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True


