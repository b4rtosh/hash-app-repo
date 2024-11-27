import hashlib
import os


def generate_hash(plain_text: str, hash_type: str, hash_salt: str = ""):
    if hash_type == "md5":
        return hashlib.md5(f"{plain_text}{hash_salt}".encode()).hexdigest()
    elif hash_type == "sha1":
        return hashlib.sha1(f"{plain_text}{hash_salt}".encode()).hexdigest()
    elif hash_type == "sha256":
        return hashlib.sha256(f"{plain_text}{hash_salt}".encode()).hexdigest()
    elif hash_type == "sha512":
        return hashlib.sha512(f"{plain_text}{hash_salt}".encode()).hexdigest()
    return None


def generate_salt(): # generate random hex string of length 16
    return os.urandom(16).hex()
