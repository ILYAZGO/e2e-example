import requests
import json
import os
import random
from datetime import datetime,timedelta, timezone

URL="https://api.stand.imot.io"

def upload_call(url, username, password):

    client_audio_path = os.path.join('audio', 'count-in.opus')
    operator_audio_path = os.path.join('audio', 'count-out.opus')

    # time for call
    #current_time = datetime.utcnow()
    current_time = datetime.now(timezone.utc)
    delta_ten = current_time + timedelta(minutes=10)
    # delta_one = current_time + timedelta(minutes=1)
    now = current_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    # one_min_later = delta_one.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    ten_min_later = delta_ten.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    print(current_time)
    print(now)

    headers_for_get_token = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data_for_user = {
        'username': username,
        'password': password,
        'scope': '',
        'client_id': '',
        'client_secret': '',
    }

    get_token_for_user = requests.post(url=url + "/token", headers=headers_for_get_token, data=data_for_user).json()

    token_for_user = f"{get_token_for_user['token_type'].capitalize()} {get_token_for_user['access_token']}"

    headers = {
        'accept': 'application/json',
        'Authorization': token_for_user,
    }

    # json
    json_data = {
        #"operator_filename": "string",
        #"bitrix_deal_id": "string",
        #"telegram_chat_id": "string",
        #"bitrix_crm_phone_number": "string",
        #"stereo_url": "string",
        #"speaker_names": ["first", "second"],
        "unique_id": f"2ceb2380baed63d{random.randint(100000,999999)}a96",
        #"bitrix_crm_entity_type": "string",
        #"bitrix_crm_entity_id": "string",
        #"bitrix_entity_type": "string",
        #"amo_note_id": "string",
        #"hangup": "client",
        "call_time": now,
        #"stereo_audio_md5": "string",
        #"answer_time": one_min_later ,
        "client_channel": 1,
        "has_audio": True,
        #"telegram_message_id": "string",
        #"bitrix_call_id": "string",
        "end_time": ten_min_later,
        #"amo_url_md5": "string",
        "operator_phone": "1234567890",
        #"operator_url": "string",
        "integration_data": {
            "integration_id": f"63ac6380baed63d{random.randint(100000,999999)}a96",
            "task_id": f"2c0bfb31-2596-49a3-8a92-19a93dbc078f",
            "service_name": "beeline"
        },
        "is_only_new_tags": False,
        #"crm_entity_id": "string",
        "unanswered": False,
        #"conversation_id": f"{random.randint(100000,999999)}",
        "is_mono": False,
        #"language": "ru",
        "tags": [
            {
                "tag_type": "upload",
                "name": "auto",
                "value": "test",
                "visible": True
            }
        ],
        "client_phone": "0987654321",
        # "multichannel_params": [
        #     {
        #         "speaker_name": "Alex",
        #         "is_operator": False,
        #         "unique_id": f"{random.randint(100000,999999)}"
        #     }
        # ],
        #"client_url": "string",
        #"client_filename": "string",
        #"amo_event_id": "string",
        "is_multichannel": False,
        "direction": "income"
    }

    # move json to string
    json_str = json.dumps(json_data)

    params = {'params': (None, json_str)}

    response = requests.post(url=URL + "/call/", headers=headers, data=params,
                             files=
                             {
                                 'client_audio': ('count-in.opus',
                                                  open(client_audio_path, 'rb'),
                                                  'audio/opus'),
                                 'operator_audio': ('count-out.opus',
                                                    open(operator_audio_path, 'rb'),
                                                    'audio/opus')
                              })

    return response.status_code, response.text


print(upload_call(URL, "auto_test_user_120323_79541", "Qaz123wsX" ))





