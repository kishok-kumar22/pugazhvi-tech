from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import JSON, ForeignKey, String, Integer, Boolean, DateTime
from config.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "auth_user"

    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    username:Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    firstname:Mapped[str] = mapped_column(String(50), nullable=False)
    lastname:Mapped[str] = mapped_column(String(50), nullable=True)
    password:Mapped[str] = mapped_column(str(400), nullable=False)
    is_active:Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser:Mapped[bool] = mapped_column(Boolean, default=False, nullable=False )
    created_by:Mapped[str] =  mapped_column(String(50), nullable=False , default="system")
    created_date:Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    last_modified_by:Mapped[str] = mapped_column(String(50), nullable=False, default="system")
    last_modified_date:Mapped[datetime] =  mapped_column(DateTime, default=datetime.now)

    # Relationship for users
    groups: Mapped[list["Groups"]] = relationship("Groups", secondary="auth_user_groups", back_populates="users")
    permissions:Mapped[list["Permissions"]] = relationship("Permissions", secondary="auth_user_group_permission", back_populates="users")

class Groups(Base):
    __tablename__ = "auth_groups"

    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    name:Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    is_active:Mapped[bool] = mapped_column(Boolean, default=True)
    created_by:Mapped[str] =  mapped_column(String(50), nullable=False)
    created_date:Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    last_modified_by:Mapped[str] = mapped_column(String(50), nullable=False)
    last_modified_date:Mapped[datetime] =  mapped_column(DateTime, default=datetime.now)

    # Relationships for Groups
    users: Mapped[list["User"]] = relationship("User", secondary="auth_user_groups", back_populates="groups")
    permissions:Mapped[list["Permissions"]] = relationship("Permissions", secondary="auth_user_group_permission", back_populates="groups")

class UserGroupsMapping(Base):
    __tablename__ = "auth_user_groups"

    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    fk_user_id:Mapped[int] = mapped_column(ForeignKey("auth_user.id", ondelete="CASCADE"), nullable=False)
    fk_group_id:Mapped[int] = mapped_column(ForeignKey("auth_groups.id", ondelete="CASCADE"), nullable=False)

class Permissions(Base):
    __tablename__ = "auth_permissions"

    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    name:Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    is_active:Mapped[bool] = mapped_column(Boolean, default=True)
    created_by:Mapped[str] =  mapped_column(String(50), nullable=False)
    created_date:Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    last_modified_by:Mapped[str] = mapped_column(String(50), nullable=False)
    last_modified_date:Mapped[datetime] =  mapped_column(DateTime, default=datetime.now)

    # Relationships for Permissions
    groups:Mapped[list["Groups"]] = relationship("Groups", secondary="auth_user_group_permission", back_populates="permissions")
    users:Mapped[list["User"]] = relationship("User", secondary="auth_user_group_permission", back_populates="permissions")

class PermissionsGroup(Base):
    __tablename__ = "auth_user_group_permission"

    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    fk_permission_id:Mapped[int] = mapped_column(ForeignKey("auth_permissions.id", ondelete="CASCADE"), nullable=False)
    fk_group_id:Mapped[int] = mapped_column(ForeignKey("auth_groups.id", ondelete="CASCADE"), nullable=False)
    fk_user_id:Mapped[int] = mapped_column(ForeignKey("auth_user.id", ondelete="CASCADE"), nullable=False)
    permissions:Mapped[dict] = mapped_column(JSON)
