from passlib.context import CryptContext


class PasswordService:
    # TODO: passlib에 bcrypt에 문제가 생긴 것 같음 버젼 호환성 문제로 추정
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def verify_password(cls, plain_password, hashed_password):
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def get_password_hash(cls, password):
        return cls.pwd_context.hash(password)
