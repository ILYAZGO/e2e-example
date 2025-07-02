import requests

ecotelecom_id = "6204e7cb599aff4f43f5d3a0"
fake_id = "123456789012345678901234" # 24 digits for every fake id if needed


def get_token(url: str, login: str, password: str):

    headers_for_get_token = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data_for_user = {
        'username': login,
        'password': password,
        'scope': '',
        'client_id': '',
        'client_secret': '',
    }
    get_token_for_user = requests.post(url=url + "/token", headers=headers_for_get_token, data=data_for_user).json()

    token_for_user = f"{get_token_for_user['token_type'].capitalize()} {get_token_for_user['access_token']}"

    return token_for_user