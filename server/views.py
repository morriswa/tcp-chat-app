
import daos


def health():
    return {
        "status": "ok",
        "msg": "hello world"
    }


def create_account(request):
    daos.create_account(request["username"], request["password"])
    return {
        "status": "ok",
        "msg": "successfully created account",
        "username": request["username"]
    }


def online_users():
    users = daos.get_online_users()
    return {
        "status": "ok",
        "msg": "successfully retrieved online users",
        "users": users
    }
