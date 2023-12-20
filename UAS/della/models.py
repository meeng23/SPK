from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class tabeltas(Base):
    __tablename__ = 'tabeltas'
    nama_tas: Mapped[str] = mapped_column(primary_key=True)
    harga: Mapped[int] = mapped_column()
    warna: Mapped[int] = mapped_column()
    ukuran: Mapped[int] = mapped_column()
    jenis : Mapped[int] = mapped_column()
    kualitas : Mapped[int] = mapped_column()
    
    def __repr__(self) -> str:
        return f"tabeltas(nama_tas={self.nama_tas!r}, harga={self.harga!r})"