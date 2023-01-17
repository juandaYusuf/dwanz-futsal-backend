# Request Method
from fastapi import APIRouter, HTTPException
from models.tabel import users, booking
from config.db import conn
from schema.schemas import User, UserRegister, LoginData, BookingData, confirmBooking


router = APIRouter()

@router.get('/admin-list')
async def getAdminList():
    return conn.execute(users.select().where(users.c.role == "admin")).fetchall()

@router.get('/client-list')
async def getClientList():
    return conn.execute(users.select().where(users.c.role == "")).fetchall()


@router.get('/{id}')
async def showWhoIsBooking(id: int):
    return conn.execute(users.select().where(users.c.id == id)).fetchall()

@router.get('/admin/{id}')
async def userAsAdmin(id: int):
    return conn.execute(users.select().where(users.c.id == id)).first()


@router.post('/login/')
async def login(data: LoginData):
    try:
        response = conn.execute(users.select().where(users.c.email == data.email, users.c.password == data.password )).first()
        email = response.email
        password = response.password
        if data.email == email and data.password == password :
            if data.userDo == 'login':
                conn.execute(users.update().values(is_active = "online").where(users.c.id == response.id))
                return response
            else :
                raise HTTPException(status_code=404, detail="Halaman tidak ditemukan")
    except AttributeError:
        raise HTTPException(status_code=404, detail="Halaman tidak ditemukan")

@router.put('/logout/{id}')
async def userLogOut( id:int ):
    conn.execute(users.update().values(is_active = "offline").where(users.c.id == id))
    response = conn.execute(users.select().where(users.c.id == id)).first()
    return response.is_active

@router.post('/register/')
async def register(user: UserRegister):
    conn.execute(users.insert().values(nik = user.nik, nama  = user.nama, email = user.email, password = user.password, nohp = user.nohp, role = " ", is_active = "offline"))
    return conn.execute(users.select()).fetchall()

@router.put('/update/{id}')
async def updateUserData(id: int, user: User):
    conn.execute(users.update().values( nama  = user.nama, email = user.email, password = user.password, nohp = user.nohp).where(users.c.id == id))
    return conn.execute(users.select().where(users.c.id == id)).first()

# !MAKE SOMEONE AS ADMIN
@router.put('/update/add-admin/{id}/{role}')
async def addAdmin(id: int, role: str):
    if(role == 'admin'):
        conn.execute(users.update().values( role = 'admin' ).where(users.c.id == id))
        return conn.execute(users.select().where(users.c.id == id)).first()
    else:
        conn.execute(users.update().values( role = ' ' ).where(users.c.id == id))
        return conn.execute(users.select().where(users.c.id == id)).first()        


# !BOOKING API
@router.post('/booking/')
async def addBookingList(booklist:BookingData):
    response = conn.execute(booking.select().order_by(booking.c.jam_selesai.asc())).first()
    # !dataFromDB ====================================================
    if not response:
        conn.execute(booking.insert().values(user_id = booklist.userID, club = booklist.club, jam_mulai = booklist.jam_mulai, jam_selesai = booklist.jam_selesai, durasi = booklist.durasi, tgl_main = booklist.tgl_main, nohp = booklist.nohp, status = booklist.status))
        return conn.execute(booking.select().where(booking.c.user_id == booklist.userID)).first()
    else:
        dbData = response.jam_selesai
        dbValue = str(dbData)
        dbResult = dbValue[0:2]
        dbFinalResult = int(dbResult)
        # !dataFromClient ================================================
        clientData = booklist.jam_mulai
        clientValue = str(clientData)
        clientResult = clientValue[0:2]
        clientFinalResult = int(clientResult)
        if clientFinalResult <= dbFinalResult:
            raise HTTPException(status_code=404, detail="Jadwal terisi")
        else:
            conn.execute(booking.insert().values(user_id = booklist.userID, club = booklist.club, jam_mulai = booklist.jam_mulai, jam_selesai = booklist.jam_selesai, durasi = booklist.durasi, tgl_main = booklist.tgl_main, nohp = booklist.nohp, status = booklist.status))
            return conn.execute(booking.select().where(booking.c.user_id == booklist.userID)).first()


@router.get('/booklist/{userID}')
async def booklist(userID:int):
    return conn.execute(booking.select().where(booking.c.user_id == userID )).fetchall()

@router.get('/admin-booklist/')
async def booklistAdmin():
    return conn.execute(booking.select()).fetchall()


@router.delete('/delete-user-booklist/{id}')
async def deleteUserBooklist(id: int):
    return conn.execute(booking.delete().where(booking.c.id == id))

# Admin Act
@router.put('/confirm/{id}')
async def confirmBooking(id: int, updateStatus : confirmBooking):
    response = conn.execute(booking.update().values(status = updateStatus.status).where(booking.c.id == id))
    return conn.execute(booking.select().where(booking.c.id == id)).first()

@router.delete('/delete-booking-list/{id}')
async def deleteBookingList(id: int):
    conn.execute(booking.delete().where(booking.c.id == id))
    response = conn.execute(booking.select().where(booking.c.id == id)).first()
    if not response :
        return 'Delete success'