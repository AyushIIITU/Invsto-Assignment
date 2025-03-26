from prisma import Prisma

db = Prisma()

def connect_db():
    if not db.is_connected():
        db.connect()
    return db

def disconnect_db():
    if db.is_connected():
        db.disconnect()