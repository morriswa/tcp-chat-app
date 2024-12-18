
def hello_world(request, authentication):
    return {
        "msg": "hello world"
    }


def error(param):
    return {
        "msg": param
    }


def create_account(request):
    return {
        "msg": "successfully created account",
        "username": request["username"]
    }
