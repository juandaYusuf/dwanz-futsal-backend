# Variable class untuk menampung data yang akang di eksekusi oleh query
from pydantic import BaseModel


# !USER
class User(BaseModel):
    nama : str
    email: str
    password: str
    nohp: str

class UserRegister(BaseModel):
    nik: str
    nama : str
    email: str
    password: str
    nohp: str

class LoginData(BaseModel):
    email: str
    password: str
    userDo: str

class BookingData(BaseModel):
    userID: int
    club: str
    jam_mulai: str
    jam_selesai: str
    durasi:int
    tgl_main: str
    nohp:str
    status:str

class confirmBooking(BaseModel):
    status:str
