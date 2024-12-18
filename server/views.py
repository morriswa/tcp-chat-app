
import daos


def health():
    return {
        "msg": "hello world"
    }


def error(param):
    return {
        "msg": param
    }


def create_account(request):
    daos.create_account(request["username"], request["password"])
    return {
        "msg": "successfully created account",
        "username": request["username"]
    }


def online_users():
    users = daos.get_online_users()
    return {
        "msg": "successfully retrieved online users",
        "users": users
    }
