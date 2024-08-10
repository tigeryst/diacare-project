import json
import os

from utils.crypt import hash_email

path_components = os.path.dirname(__file__).split(os.sep)
root_index = path_components.index("app")
root_dir = os.sep.join(path_components[: root_index + 1])
profile_dir = os.path.join(root_dir, "profiles")


def update_user(user_data):
    email = user_data["email"]
    hashed_email = hash_email(email)
    file_path = os.path.join(profile_dir, f"{hashed_email}.json")
    with open(file_path, "r+") as file:
        print(file)
        existing_data = json.load(file)
        print(existing_data)
        hashed_password = existing_data["password"]
        new_data = {
            "email": email,
            "password": hashed_password,
            **user_data,
        }
        print(new_data)
        file.seek(0)
        json.dump(new_data, file)


def get_user(email):
    hashed_email = hash_email(email)
    file_path = os.path.join(profile_dir, f"{hashed_email}.json")
    with open(file_path, "r") as file:
        user_data = json.load(file)
        return user_data
