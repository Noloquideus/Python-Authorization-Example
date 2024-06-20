import uuid
from sqlalchemy import Column, UUID, String, Boolean, Integer
from sqlalchemy.dialects.postgresql import ARRAY
from src.infrastructure.database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    username = Column(String, nullable=False, unique=True, index=True)
    password_hash = Column(String, nullable=False)
    access_level = Column(Integer, nullable=False, default=1)
    is_email_verified = Column(Boolean, nullable=False, default=False)
    refresh_tokens = Column(ARRAY(String), nullable=True)
