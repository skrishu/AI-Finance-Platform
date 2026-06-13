import bcrypt
from database.db import SessionLocal
from database.models import User


def hash_password(password):

    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()



def create_user(name, email, password):

    db = SessionLocal()


    existing = db.query(User).filter(
        User.email == email
    ).first()


    if existing:
        return False


    user = User(
        name=name,
        email=email,
        password=hash_password(password)
    )


    db.add(user)
    db.commit()

    db.close()

    return True



def login_user(email,password):

    db = SessionLocal()


    user = db.query(User).filter(
        User.email == email
    ).first()


    db.close()


    if user:

        if bcrypt.checkpw(
            password.encode(),
            user.password.encode()
        ):
            return user


    return None