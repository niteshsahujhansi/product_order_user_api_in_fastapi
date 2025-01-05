
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from models import User as UserModel
from schemas import UserInDB
from models import Base

DATABASE_URL = "postgresql://postgres:root@localhost/thepointy"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



def get_user(db: Session, username: str) -> UserInDB | None:
    user = db.query(UserModel).filter(UserModel.username == username).first()
    if user:
        return UserInDB(
            id=user.id,
            username=user.username,
            full_name=user.full_name,
            email=user.email,
            hashed_password=user.hashed_password,
            disabled=user.disabled,
        )
    return None


# Create all tables in the database
Base.metadata.create_all(bind=engine)