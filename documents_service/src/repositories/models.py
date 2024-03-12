from sqlalchemy import UUID, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Document(Base):
    __tablename__ = "documents"

    id = mapped_column(UUID(as_uuid=True), primary_key=True)
    name = mapped_column(String, nullable=False, unique=False)
    text = mapped_column(Text)
    vault_id = mapped_column(ForeignKey("vaults.id"), nullable=False)    

    vaults = relationship("Vault", back_populates="documents")


class Vault(Base):
    __tablename__ = "vaults"

    id = mapped_column(UUID(as_uuid=True), primary_key=True)
    name = mapped_column(String, nullable=False, unique=False)
    type = mapped_column(String, nullable=False, unique=False)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    user_id = mapped_column(UUID(as_uuid=True), nullable=False)

    documents = relationship("Document", back_populates="vaults")
