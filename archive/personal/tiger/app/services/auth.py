import json
import os

from utils.crypt import hash_email, hash_password, verify_password

path_components = os.path.dirname(__file__).split(os.sep)
root_index = path_components.index("app")
root_dir = os.sep.join(path_components[: root_index + 1])
profile_dir = os.path.join(root_dir, "profiles")

if not os.path.exists(profile_dir):
    os.makedirs(profile_dir)


def register(email, password):
    hashed_email = hash_email(email)
    hashed_password = hash_password(password)
    file_path = os.path.join(profile_dir, f"{hashed_email}.json")

    if os.path.exists(file_path):
        raise Exception("User already exists")
    else:
        user_data = {
            "email": email,
            "password": hashed_password,
        }
        with open(file_path, "w") as file:
            json.dump(user_data, file)


def login(email, password):
    hashed_email = hash_email(email)
    file_path = os.path.join(profile_dir, f"{hashed_email}.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            user_data = json.load(file)
            if verify_password(password, user_data["password"]):
                return
    raise Exception("Invalid email or password")
