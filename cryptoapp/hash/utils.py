import hashlib


def hash_string_sha256(palin_text: str, salt: str = ""):
    if str:
        return hashlib.sha256(f"{palin_text}{salt}".encode()).hexdigest()


def hash_string_sha512(palin_text: str, salt: str = ""):
    if str:
        return hashlib.sha512(f"{palin_text}{salt}".encode()).hexdigest()


def hash_string_md5(palin_text: str, salt: str = ""):
    if str:
        return hashlib.md5(f"{palin_text}{salt}".encode()).hexdigest()


def hash_string_sha1(palin_text: str, salt: str = ""):
    if str:
        return hashlib.sha1(f"{palin_text}{salt}".encode()).hexdigest()

