from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from jose import jwt, JWTError
from app.config.settings import settings


class AbstractJWTEncoder(ABC):
    """
    JWT 인코더 추상클래스
    encode 메소드를 구현

    :param data: JWT에 담을 데이터
    :param expires_delta: JWT 만료 시간
    :param secret_key: JWT 암호화 키
    :param algorithm: JWT 암호화 알고리즘
    """

    @abstractmethod
    def encode(self, data: dict, expires_delta: int, secret_key: str, algorithm: str) -> str:
        pass


class AbstractJWTDecoder(ABC):
    """
    JWT 디코더 추상클래스
    decode 메소드를 구현

    :param token: JWT 토큰
    :param secret_key: JWT 암호화 키
    :param algorithm: JWT 암호화 알고리즘
    """

    @abstractmethod
    def decode(self, token: str, secret_key: str, algorithm: str) -> dict | None:
        pass


class JWTEncoder(AbstractJWTEncoder):
    def encode(self, data: dict, expires_delta: int, secret_key: str, algorithm: str) -> str:
        to_encode = data.copy()
        expire = datetime.now(ZoneInfo("Asia/Seoul")) + timedelta(minutes=expires_delta)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, secret_key, algorithm=algorithm)


class JWTDecoder(AbstractJWTDecoder):
    def decode(self, token: str, secret_key: str, algorithm: str) -> dict | None:
        try:
            return jwt.decode(token, secret_key, algorithms=[algorithm])
        except JWTError:
            return None


class JWTService:
    """
    JWT 로그인시 access token, refresh token을 생성하는 로직
    """

    def __init__(
        self,
        encoder: JWTEncoder,
        decoder: JWTDecoder,
        algorithm: str = None,
        secret_key: str = None,
        access_token_expire_time: int = None,
        refresh_token_expire_time: int = None,
    ):
        self.encoder = encoder
        self.decoder = decoder
        self.algorithm = algorithm
        self.secret_key = secret_key
        self.access_token_expire_time = access_token_expire_time
        self.refresh_token_expire_time = refresh_token_expire_time

    def create_access_token(self, data: dict) -> str:
        return self._create_token(data, self.access_token_expire_time)

    def create_refresh_token(self, data: dict) -> str:
        return self._create_token(data, self.refresh_token_expire_time)

    def _create_token(self, data: dict, expires_delta: int) -> str:
        return self.encoder.encode(data, expires_delta, self.secret_key, self.algorithm)

    def check_token_expired(self, token: str) -> dict | None:
        payload = self.decoder.decode(token, self.secret_key, self.algorithm)

        now = datetime.timestamp(datetime.now(settings.TIMEZONE))
        if payload and payload["exp"] < now:
            return None

        return payload


jwt_service = JWTService(
    encoder=JWTEncoder(),
    decoder=JWTDecoder(),
    algorithm=settings.JWT_ALGORITHM,
    secret_key=settings.JWT_SECRET_KEY,
    access_token_expire_time=settings.JWT_ACCESS_TOKEN_EXPIRE_TIME,
    refresh_token_expire_time=settings.JWT_REFRESH_TOKEN_EXPIRE_TIME,
)
