import bcrypt

# bcrypt 只使用前 72 字节，超出部分会被忽略，这里显式截断以避免 bcrypt 5 抛错
_BCRYPT_MAX_BYTES = 72


def _to_bcrypt_bytes(password: str) -> bytes:
    return password.encode("utf-8")[:_BCRYPT_MAX_BYTES]


# 密码加密
def get_hash_password(password: str) -> str:
    return bcrypt.hashpw(_to_bcrypt_bytes(password), bcrypt.gensalt()).decode("utf-8")


# 密码校验
def verify_password(password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(_to_bcrypt_bytes(password), hashed_password.encode("utf-8"))
    except ValueError:
        return False
