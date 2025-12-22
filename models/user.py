from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime, Date
from sqlalchemy.orm import validates, relationship
from core.database import Base
import re

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), index=True)
    email = Column(String(100), unique=True, index=True)
    phone = Column(String(20), unique=True, nullable=True, index=True)
    gender = Column(Enum("male", "female", name="gender_enum"), nullable=True)
    birthdate = Column(Date, nullable=True)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    avatar_url = Column(String(255), nullable=True)
    role = Column(Enum("user", "admin", "moderator", name="role_enum"), default="user")
    last_login = Column(DateTime, nullable=True)
    last_update = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False)
    wishlist = relationship("Wishlist", back_populates="user", cascade="all, delete")


    @validates('phone')
    def validate_phone(self, key, phone):
        if phone is None:
            return phone
        
        # Sadece rakamlar, 10-15 karakter
        if not re.match(r'^[0-9]{10,15}$', phone):
            raise ValueError("Telefon numarası 10-15 haneli rakamlardan oluşmalıdır")
        
        return phone
    
    @validates('email')
    def validate_email(self, key, email):
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValueError("Geçerli bir email adresi giriniz")
        return email

    def to_json(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "gender": self.gender,
            "birthdate": self.birthdate.isoformat() if self.birthdate else None,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "avatar_url": self.avatar_url,
            "role": self.role,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "created_at": self.created_at.isoformat(),
            "last_update": self.last_update.isoformat() if self.last_update else None
        }