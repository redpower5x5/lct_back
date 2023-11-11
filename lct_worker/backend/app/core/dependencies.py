from app.core.database import SessionLocal
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer


# region db


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# endregion

# region password

pwd_context = CryptContext(schemes=["bcrypt"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/token")

# endregion
