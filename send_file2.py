import os
import json
import requests
from datetime import datetime
import random


IMOT_TOKEN = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiNjRmNzIyZmI4YzAzMWU5YzM5M2EyMTA0IiwiZXhwIjoxNzQwNTA0Nzg5fQ.6WJ--9AcGMNT7W7A6LPXZ9LhYvR6eXdAMNOw-Nf7KVI' # нужно вставить сюда API ключ.
UPLOAD_ENDPOINT = 'https://api.stand.imot.io/call/'
CHECK_ENDPOINT = 'https://api.stand.imot.io/find_call'
unique_id= f"2ceb2380bahg63d{random.randint(100000,999999)}a96"

def upload_call_to_imotio(
        token: str,
        unique_id: str,          # ID звонка в системе клиента,
                                 #   IMOT.IO проверяет уникальность этого поля при загрузке
        call_time: datetime,     # время совершения звонка
        filename: str,           # имя файла который нужно загрузить
        client_channel: int = 0, # номер канала в котором говорит клиент, для стерео файла,
                                 #    если клиент в правом ухе нужно передавать 1
        client_phone: str = '',  # номер телефона клиента
        operator_phone: str = '',# номер телефона сотрудника
        meta_data: dict = None   # Мета данные о звонке. Произвольный набор данных,
                                 #    в IMOT.IO отображаются как теги звонка
) -> str:
    """
    Выполняет загрузку файла в сервис IMOT.IO
    Возвращает ID звонка в сервисе
    При повторном вызове для сушествующего звонка функия возврашает сушествующий ID звонка.
    Если загрузка по какой-то причине не удалась, функция кидает исключения.
    """

    if not unique_id:
        raise ValueError("unique_id required")

    if not IMOT_TOKEN:
        raise ValueError("Fill value IMOT_TOKEN to make requests")

    headers = {'Authorization': token}

    req = requests.get(f"{CHECK_ENDPOINT}/{unique_id}", headers=headers)
    if req.status_code == 200:
        # Звонок уже существует
        response = req.json()
        if 'call_id' not in response:
            raise RuntimeError(f"{CHECK_ENDPOINT} don't return call_id. Response: {response}")

        return response['call_id']

        # update params
    elif req.status_code != 404:
        # другой ответ от imot.io который неожиданен для нас.
        req.raise_for_status()

    # мы дошли до сюда после того как IMOT.IO адекватно ответил, что такого звонка у него нет

    # Define the correct path to the file
    filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio/stereo.opus")

    # Ensure the path is absolute
    filename = os.path.abspath(filename)

    if not os.path.isfile(filename):
        raise ValueError(f"{filename=} is not valid file")

    files = {"stereo_audio": (os.path.basename(filename), open(filename, 'rb'))}

    tags = []
    if meta_data:
        for k,v in meta_data.items():
            if v:
                tags.append({"name": str(k), "value": str(v)})
            else:
                tags.append({"name": str(k)})


    params = {'call_time': call_time.timestamp(),
              'client_phone': client_phone,
              'operator_phone': operator_phone,
              'client_channel': client_channel,
              'unique_id': unique_id,
              'tags': tags,
    }

    req = requests.post(
            UPLOAD_ENDPOINT,
            files=files,
            data={'params': json.dumps(params)},
            headers=headers
    )
    req.raise_for_status()
    response = req.json()
    return response

if __name__ == '__main__':
    try:
        call_id = upload_call_to_imotio(
                token=IMOT_TOKEN,
                unique_id=unique_id,
                call_time = datetime(2025, 2, 10, 13, 15, 0),
                filename='stereo.opus',
                client_phone = '+79031112233',
                operator_phone = '102',
                meta_data = {'Сотрудник': 'Вася',
                             'Отдел': 'Продажи',
                             'Направление звонка': 'Входящий',
                             'ID сотрудника': 123,
                             'Холодный обзвон': '',  # значение может быть пустым,
                                                     # это превратится в тег без значения
                            })
        print(f"Call uploaded: {call_id}")
    except Exception as e:
        print(f"Failed to upload: {e}")
        import traceback
        traceback.print_exc()