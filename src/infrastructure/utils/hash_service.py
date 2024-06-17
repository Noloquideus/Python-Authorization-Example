import bcrypt


class HashService:
    @staticmethod
    def hash(password: str) -> str:
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return hashed_password.decode()

    @staticmethod
    def verify(hashed_password: str, plain_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
