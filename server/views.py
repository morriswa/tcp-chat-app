
import daos


def health():
    return {
        "status": "ok",
        "msg": "hello world",
        "body": None
    }


def create_account(request):
    daos.create_account(request["username"], request["password"])
    return {
        "status": "ok",
        "msg": "successfully created account",
        "body": request["username"]
    }


def online_users():
    users = daos.get_online_users()
    return {
        "status": "ok",
        "msg": "successfully retrieved online users",
        "body": users
    }


def send_message(request, auth):
    uname_to = request["username"]
    message = request["message"]
    daos.send_message(auth, uname_to, message)
    return {
        "status": "ok",
        "msg": "successfully sent message",
        "body": None
    }


def get_chat_history(request, auth):
    uname_to = request["username"]
    chats = daos.get_chat_history(auth, uname_to)
    return {
        "status": "ok",
        "msg": "successfully retrieved messages",
        "body": [chat.json() for chat in chats]
    }


def get_active_chats(request, auth):
    users = daos.get_active_chats(auth)
    return {
        "status": "ok",
        "msg": "successfully retrieved active chats",
        "body": users
    }
