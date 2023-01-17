# Membuat tabel database
from sqlalchemy import Date, ForeignKey, Integer, String, Table, Column, Time
from config.db import engine, metaData 

users = Table(
    'users',
    metaData,
    Column('id', Integer, primary_key=True),
    Column('nik', String(50)),
    Column('nama', String(30)),
    Column('email', String(255)),
    Column('password', String(100)),
    Column('nohp', String(20)),
    Column('role', String(5)),
    Column('is_active', String(7))
    )

booking = Table(
    'booking',
    metaData,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey("users.id"), nullable=False),
    Column('club', String(255)),
    Column('jam_mulai', Time),
    Column('jam_selesai', Time),
    Column('durasi', Integer),
    Column('tgl_main', Date),
    Column('nohp', String(20)),
    Column('status',String(10))
)

# lapang = Table(
#     'lapang',
#     metaData,
#     Column('id', Integer, primary_key=True),
#     Column('booking_id', Integer, ForeignKey('booking.id'), nullable=False),
#     Column('jam_quota', String(2))
# )

metaData.create_all(engine)