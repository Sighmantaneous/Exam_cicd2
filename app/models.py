from sqlalchemy  import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class EquipmentDB(Base):
    __tablename__ = "equipment"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    equipment_id: Mapped[int] = mapped_column(nullable=False, unique=True)
    borrower_name: Mapped[str] = mapped_column(String(60),nullable=False)
    loan_days: Mapped[int] = mapped_column(nullable=False)
    purpose: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(default="Pending")
