import bcrypt
import hashlib
import base64


def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


def hash_email(email):
    hash_object = hashlib.md5(email.encode("utf-8"))
    hash_digest = hash_object.digest()
    encoded_hash = base64.urlsafe_b64encode(hash_digest)
    return encoded_hash.decode("utf-8")
