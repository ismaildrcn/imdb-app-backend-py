

from dataclasses import dataclass
from typing import Optional
from models.user import User

@dataclass
class UserDto:

    id: Optional[int]
    full_name: str
    email: str
    phone: Optional[str] = None
    gender: Optional[str] = None
    birthdate: Optional[str] = None  # ISO format date string
    avatar_url: Optional[str] = None
    is_verified: Optional[bool] = False

    @staticmethod
    def from_entity(user: User) -> 'UserDto':
        return UserDto(
            id=user.id,
            full_name=user.full_name,
            email=user.email,
            phone=user.phone,
            gender=user.gender,
            birthdate=user.birthdate,
            avatar_url=user.avatar_url,
            is_verified=user.is_verified
        )