import requests as r
import random
import time
from utils.dates import today
from send_file2 import upload_call_to_imotio
from datetime import datetime, timedelta, timezone
from loguru import logger

logger.remove()
logger.add(sink='exec.log', level='INFO', rotation='10 MB', compression='zip', diagnose=True)

'''for create user write before test :
USER_ID, BEARER, ACCESS_TOKEN = create_user(API_URL, ROLE_..., PASSWORD)

optional flags if needed

for delete user write after test :
delete_user(API_URL, TOKEN, USER_ID)'''


def create_user(url: str, role: str, password: str,
                gpt_rule=False,
                upload_call=False,
                create_report=False,
                deal_check_list=False,
                create_many_rules=False,
                rules_name="AT_many_rules",
                rules_entity="CALL",
                rule_value="",
                rules_amount=5,
                phrases_and_dicts=None,
                create_many_dicts=False,
                dicts_name="AT_many_dicts",
                dicts_amount=5,
                retag=False
                ):

    if phrases_and_dicts is None:
        phrases_and_dicts = []

    # get token for 4adminIM. All users will be created by 4adminIM
    headers_for_get_token = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = {
        'username': '*******',
        'password': '*******'
    }

    get_token = r.post(f"{url}/token", headers=headers_for_get_token, data=data).json()

    #token = f"{get_token['token_type'].capitalize()} {get_token['access_token']}"
    token = f"Bearer {get_token['access_token']}"

    # create user
    name = login = f"auto_test_user_{datetime.now().strftime('%m%d%H')}_{random.randint(100, 99999)}"

    headers_for_create = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': token,
    }

    json_for_create = {
        'role': role,
        'login': login,
        'name': name,
        'password': password,
        "makeDeals": True,
        "sttOptions": {
            "sttEngine": "vosk",
            "sttEconomize": False,
            "sttOptionsMap":
                {"language": "ru-RU",
                 "model": "default",
                 "merge_all_to_one_audio": False,
                 "count_per_iteration": 1,
                 "diarization": False}
        }
    }

    create = r.post(f"{url}/user", headers=headers_for_create, json=json_for_create)
    user_id = create.text.replace('"', '')

    if create.status_code == 200:
        logger.opt(depth=1).info(f"\n>>>>> USER {name} WITH user_id: {user_id} CREATED SUCCESSFULLY <<<<<")
    else:
        logger.opt(depth=1).info(f"\n>>>>> ERROR CREATE USER {create.status_code} {create.text}<<<<<")

    if role == 'user':

        # giving quota if user
        quota = {
            "time_nominal": 46620
        }

        give_quota = r.post(url=url + f"/user/{user_id}/quota", headers=headers_for_create, json=quota)

        if give_quota.status_code == 200:
            logger.opt(depth=1).info(f"\n>>>>> USER {name} WITH user_id: {user_id} IS GIVEN A QUOTA OF 777 MINUTES <<<<<")
        else:
            logger.opt(depth=1).info(f"\n>>>>> ERROR GIVING QUOTA {give_quota.status_code} <<<<<")

        # giving gpt quota
        gpt_quota = [{"key":"imotio_gpt","day_limit":1000}]

        give_gpt_quota = r.patch(url=url + f"/user/{user_id}/gpt_quotas", headers=headers_for_create, json=gpt_quota)

        if give_gpt_quota.status_code == 204:
            logger.opt(depth=1).info(f"\n>>>>> USER {name} WITH user_id: {user_id} IS GIVEN GPT QUOTA OF 1000 PER DAY <<<<<")
        else:
            logger.opt(depth=1).info(f"\n>>>>> ERROR GIVING GPT QUOTA {give_gpt_quota.status_code} <<<<<")

        # get token for user
        ##get token
        data_for_user = {
            'username': name,
            'password': password
        }
        get_token_for_user = r.post(f"{url}/token", headers=headers_for_get_token, data=data_for_user).json()

        token_for_user = f"{get_token_for_user['token_type'].capitalize()} {get_token_for_user['access_token']}"

        headers_for_user = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': token_for_user,
        }

        # create communication check list
        call_check_list = {
            "enabledUsers":[],
            "title":"auto_call_ch_list",
            "entityType":"CALL",
            "enabled":True,
            "priority":0,
            "globalFilter":
                {
                    "title":None,"items":[]
                },
            "questions":[
                {"id":"",
                 "text":"q1",
                 "answerValues":["a1"],
                 "answerAutoSelectSearchFilters":{"a1":{"title":None,"items":[{"key":"any_of_tags","values":["auto_rule"]}]}},
                 "answerSelectedTaggingLogic":{"a1":[{"strategyOnSet":"ADD","strategyOnUnset":"REMOVE","tags":["auto_rule"]}]},
                 "answerPoints":{"a1":10}},
                {"id":"",
                 "text":"q2",
                 "answerValues":["a2"],
                 "answerAutoSelectSearchFilters":{"a2":{"title":None,"items":[{"key":"any_of_tags","values":["auto_rule"]}]}},
                 "answerSelectedTaggingLogic":{"a2":[{"strategyOnSet":"ADD","strategyOnUnset":"REMOVE","tags":["auto_rule"]}]},
                 "answerPoints":{"a2":-10}}
            ],
            "appraisers":[],
            "generateReport":False
        }

        add_call_check_list = r.post(f"{url}/checklists/", headers=headers_for_user, json=call_check_list)
        call_check_list_id = add_call_check_list.text.replace('"', '')

        if add_call_check_list.status_code == 200:
            logger.opt(depth=1).info(
                f"\n>>>>> FOR USER {name} CREATED communication check list {call_check_list_id}<<<<<")
        else:
            logger.opt(depth=1).info(
                f"\n>>>>> ERROR CREATING CHECKLIST {add_call_check_list.status_code} <<<<<")


        # create deal check list
        if deal_check_list:
            deal_check_list = {
                "enabledUsers":[],
                "title":"auto_deal_ch_list",
                "entityType":"DEAL",
                "enabled":True,
                "priority":0,
                "globalFilter":
                    {
                        "title":None,"items":[]
                    },
                "questions":[
                    {"id":"",
                     "text":"q1",
                     "answerValues":["a1"],
                     "answerAutoSelectSearchFilters":{"a1":{"title":None,"items":[{"key":"any_of_tags","values":["auto_rule"]}]}},
                     "answerSelectedTaggingLogic":{"a1":[{"strategyOnSet":"ADD","strategyOnUnset":"REMOVE","tags":["auto_rule"]}]},
                     "answerPoints":{"a1":100}},
                    {"id":"",
                     "text":"q2",
                     "answerValues":["a2"],
                     "answerAutoSelectSearchFilters":{"a2":{"title":None,"items":[{"key":"any_of_tags","values":["auto_rule"]}]}},
                     "answerSelectedTaggingLogic":{"a2":[{"strategyOnSet":"ADD","strategyOnUnset":"REMOVE","tags":["auto_rule"]}]},
                     "answerPoints":{"a2":-10}}
                ],
                "appraisers":[],
                "generateReport":False
            }

            add_deal_check_list = r.post(f"{url}/checklists/", headers=headers_for_user, json=deal_check_list)
            deal_check_list_id = add_deal_check_list.text.replace('"', '')

            if add_deal_check_list.status_code == 200:
                logger.opt(depth=1).info(
                    f"\n>>>>> FOR USER {name} CREATED deal check list {deal_check_list_id}<<<<<")
            else:
                logger.opt(depth=1).info(
                    f"\n>>>>> ERROR CREATING CHECKLIST {add_deal_check_list.status_code} <<<<<")

        else:
            pass

        # create gpt rule
        if gpt_rule:
            gpt_rule = {
                "engine":"imotio_gpt",
                "model":"auto",
                "systemText":"",
                "userTextTemplate":"",
                "temperature":"0",
                "title":"auto_gpt_rule",
                "simpleQuestions":
                    [
                        {"question":"If there's text in the call, make the tag “text”.",
                         "tagName":"question_name",
                         "isComment":False,
                         "isTag":True,
                         "tagSeparators":"",
                         "priority":0,
                         "yamlKey":""
                         }
                    ]
            }

            add_gpt_rule = r.post(f"{url}/gpt/", headers=headers_for_user, json=gpt_rule)
            gpt_rule_id = add_gpt_rule.text.replace('"', '')

            if add_gpt_rule.status_code == 200:
                logger.opt(depth=1).info(
                    f"\n>>>>> FOR USER {name} CREATED communication check list {gpt_rule_id}<<<<<")
            else:
                logger.opt(depth=1).info(
                    f"\n>>>>> ERROR CREATING CHECKLIST {add_gpt_rule.status_code} <<<<<")
        else:
            pass

        #create groups
        rule_group = {
            "title": "auto_rule_group",
            "enabled": True
        }
        dict_group = {
            "title": "auto_dict_group",
            "enabled": True
        }
        add_rule_group = r.post(f"{url}/tag_rule_group/", headers=headers_for_user, json=rule_group)
        add_dict_group = r.post(f"{url}/dict_group/", headers=headers_for_user, json=dict_group)

        rule_group_id = add_rule_group.text.replace('"', '')
        dict_group_id = add_dict_group.text.replace('"', '')

        if add_rule_group.status_code == 201:
            logger.opt(depth=1).info(f"\n>>>>> FOR USER {name} WITH user_id: {user_id} CREATED RULE GROUP {rule_group_id} <<<<<")
        else:
            logger.opt(depth=1).info(f"\n>>>>> ERROR CREATING RULE GROUP {add_rule_group.status_code} <<<<<")

        if add_dict_group.status_code == 201:
            logger.opt(depth=1).info(
                f"\n>>>>> FOR USER {name} WITH user_id: {user_id} CREATED DICT GROUP {dict_group_id} <<<<<")
        else:
            logger.opt(depth=1).info(f"\n>>>>> ERROR CREATING DICT GROUP {add_dict_group.status_code} <<<<<")

        #create rule and dict in groups
        rule = {
            "owner": user_id,
            "title": "auto_rule",
            "group": rule_group_id,
            "enabled": True,
            "calculatedRulePriority": 0,
            "globalFilter": [],
            "fragmentRules": [{"phrasesAndDicts": [], "phrases": [], "dicts": [],
                              "direction": "", "fromStart": False, "silentBefore": "",
                              "silentAfter": "", "interruptTime": "", "talkBefore": "",
                               "talkAfter": "", "onlyFirstMatch": False, "fragmentsBefore": "",
                               "fragmentsAfter": "", "distancePrevRuleTime": "", "distancePrevRuleFragmentCount": "",
                               "orPhrasesAndDicts": [], "orPhrases": [], "orDicts": [], "orDirection": ""}],
            "setTags": [{"name": "auto_rule", "value": "", "visible": False}],
            "allowedActions": [],
            "timeTagRules": []}

        add_rule = r.post(f"{url}/tag_rule/", headers=headers_for_user, json=rule)

        rule_id = add_rule.text.replace('"', '')

        if add_rule.status_code == 201:
            logger.opt(depth=1).info(f"\n>>>>> FOR USER {name} WITH user_id: {user_id} CREATED RULE {rule_id} INSIDE GROUP {rule_group_id} <<<<<")
        else:
            logger.opt(depth=1).info(f"\n>>>>> ERROR CREATING RULE {add_rule.status_code} <<<<<")

        dict = {"title": "auto_dict",
                "owner": user_id,
                "enabled": True,
                "group": dict_group_id,
                "usedRules": [],
                "allowedUsers": [],
                "phrases": ["auto_dict"]}

        add_dict = r.post(f"{url}/dict/", headers=headers_for_user, json=dict)
        dict_id = add_dict.text.replace('"', '')

        if add_dict.status_code == 201:
            logger.opt(depth=1).info(
                f"\n>>>>> FOR USER {name} WITH user_id: {user_id} CREATED auto_dict {dict_id} INSIDE GROUP {dict_group_id} <<<<<")
        else:
            logger.opt(depth=1).info(
                f"\n>>>>> ERROR CREATING DICT {add_dict.status_code} DICT auto_dict<<<<<")

        # create many rules
        if create_many_rules:
            rule_group = {
                "title": "AT_rules_group",
                "enabled": True
            }
            add_rule_group = r.post(f"{url}/tag_rule_group/", headers=headers_for_user, json=rule_group)
            group_id = add_rule_group.text.replace('"', '')

            if add_rule_group.status_code == 201:
                logger.opt(depth=1).info(f"\n>>>>> FOR USER {name} CREATED RULE GROUP {group_id} <<<<<")
            else:
                logger.opt(depth=1).info(f"\n>>>>> ERROR CREATING RULE GROUP {add_rule_group.status_code}<<<<<")

            for i in range(1, rules_amount + 1):
                rule = {
                    "owner": user_id,
                    "title": f"{rules_name}{i}",
                    "entityType": rules_entity,
                    "group": group_id,
                    "enabled": True,
                    "rulePriority": i,
                    "calculatedRulePriority": i,
                    "globalFilter": [],
                    "fragmentRules": [{"phrasesAndDicts": phrases_and_dicts, "phrases": [], "dicts": [],
                                       "direction": "", "fromStart": False, "silentBefore": "",
                                       "silentAfter": "", "interruptTime": "", "talkBefore": "",
                                       "talkAfter": "", "onlyFirstMatch": False, "fragmentsBefore": "",
                                       "fragmentsAfter": "", "distancePrevRuleTime": "",
                                       "distancePrevRuleFragmentCount": "",
                                       "orPhrasesAndDicts": [], "orPhrases": [], "orDicts": [], "orDirection": ""}],
                    "setTags": [{"name": f"{rules_name}{i}tag", "value": f"{rule_value}", "visible": False}],
                    "allowedActions": [],
                    "timeTagRules": []}

                add_rule = r.post(url=url + "/tag_rule/", headers=headers_for_user, json=rule)
                rule_id = add_rule.text.replace('"', '')

                if add_rule.status_code == 201:
                    logger.opt(depth=1).info(
                        f"\n>>>>> FOR USER {name} CREATED {rules_name}{i} {rule_id} INSIDE GROUP {group_id} <<<<<")
                else:
                    logger.opt(depth=1).info(
                        f"\n>>>>> ERROR CREATING RULE {add_rule.status_code} RULE NAME {rules_name}{i} {add_rule.text}<<<<<")

        # create many dicts
        if create_many_dicts:
            dict_group = {
                "title": "AT_dicts_group",
                "enabled": True
            }
            add_dict_group = r.post(url=url + "/dict_group/", headers=headers_for_user, json=dict_group)
            group_id = add_dict_group.text.replace('"', '')

            if add_dict_group.status_code == 201:
                logger.opt(depth=1).info(
                    f"\n>>>>> FOR USER {login} WITH user_id: {user_id} CREATED DICT GROUP {group_id} <<<<<")
            else:
                logger.opt(depth=1).info(f"\n>>>>> ERROR CREATING DICT GROUP {add_dict_group.status_code} <<<<<")

            for i in range(1, dicts_amount + 1):
                dictionary = {
                    "title": f"{dicts_name}{i}",
                    "owner": user_id,
                    "enabled": True,
                    "group": group_id,
                    "usedRules": [],
                    "allowedUsers": [],
                    "phrases": [f"{dicts_name}{i}"]
                }

                add_dict = r.post(url=url + "/dict/", headers=headers_for_user, json=dictionary)
                dict_id = add_dict.text.replace('"', '')

                if add_dict.status_code == 201:
                    logger.opt(depth=1).info(
                        f"\n>>>>> FOR USER {name} CREATED {dicts_name}{i} {dict_id} INSIDE GROUP {group_id} <<<<<")
                else:
                    logger.opt(depth=1).info(
                        f"\n>>>>> ERROR CREATING DICT {add_dict.status_code} DICT NAME {dicts_name}{i}<<<<<")

        # do retag
        if retag:
            analyze_data = {
                "start_date": today.strftime("%Y-%m-%d"),
                "end_date": today.strftime("%Y-%m-%d"),
                "action": "analyze"
            }
            analyze_task = r.post(f"{url}/calls/action", headers=headers_for_user, json=analyze_data)

            if analyze_task.status_code == 200:
                logger.opt(depth=1).info(f"\n retag started")
            else:
                logger.opt(depth=1).info(
                    f"\n retag was not started {analyze_task.status_code}")
        else:
            pass

        # create report for user
        if create_report:
            report_name = f"auto_test_report_{random.randint(1000, 999999)}"

            json_for_create_report = {
                "report_id": None,
                "report_name": report_name,
                "report_type": "calls",
                "from_time": None,
                "to_time": None,
                "call_search_items": [],
                "view_options": {
                    "show_table": True,
                    "show_chart": False,
                    "show_diff_report": False,
                    "show_zero_rows": True,
                    "show_zero_cols": True,
                    "show_zero_grouping_rows": True,
                    "show_zero_grouping_cols": True,
                    "show_row_calls_sum": True,
                    "show_col_calls_sum": True,
                    "show_row_all_calls_sum": False,
                    "show_col_all_calls_sum": False,
                    "show_row_calls_missed": False,
                    "show_col_calls_missed": False,
                    "chart_options": {
                        "by_sub_column": "calls_count",
                        "chart_type": "histogram"
                    }
                },
                "rows_group_by": [
                    {
                        "group_by": "time",
                        "value": "day" ,
                        "view_options": {
                            "show_calls_count": True,
                            "show_minutes": False,
                            "show_percentage": False,
                            "show_operator_time": False,
                            "show_percentage_from_all_calls_row": False,
                            "show_percentage_from_all_calls_col": False,
                            "show_percentage_from_sum_calls_row": False,
                            "show_percentage_from_sum_calls_col": False,
                            "show_client_time": False,
                            "show_silence_time": False,
                            "show_operator_time_percentage": False,
                            "show_client_time_percentage": False,
                            "show_silence_time_percentage": False,
                            "show_call_dt": False,
                            "show_tags_count": False,
                            "show_deals": False,
                            "show_checklist_average": False,
                            "show_checklist_average_percent": False,
                            "show_client_phones": False,
                            "show_operator_phones": False,
                            "show_points": False,
                            "show_max_points": False,
                            "show_from_services": False,
                            "additional_params": []
                        }
                    }
                ],
                "cols_group_by": [
                    {
                        "group_by": "calls_count",
                        "view_options": {
                            "show_calls_count": True,
                            "show_minutes": False,
                            "show_percentage": False,
                            "show_operator_time": False,
                            "show_percentage_from_all_calls_row": False,
                            "show_percentage_from_all_calls_col": False,
                            "show_percentage_from_sum_calls_row": False,
                            "show_percentage_from_sum_calls_col": False,
                            "show_client_time": False,
                            "show_silence_time": False,
                            "show_operator_time_percentage": False,
                            "show_client_time_percentage": False,
                            "show_silence_time_percentage": False,
                            "show_call_dt": False,
                            "show_tags_count": False,
                            "show_deals": False,
                            "show_checklist_average": False,
                            "show_checklist_average_percent": False,
                            "show_client_phones": False,
                            "show_operator_phones": False,
                            "show_points": False,
                            "show_max_points": False,
                            "show_from_services": False,
                            "additional_params": []
                        }
                    }
                ],
                "period": "all_time",
                "from_dt": None,
                "to_dt": None
            }

            # create report
            url_for_create_report = f'{url}/reports'

            create_report = r.post(url_for_create_report, headers=headers_for_user, json=json_for_create_report)

            report_id = create_report.text.replace('"', '')

            if create_report.status_code == 200:
                logger.opt(depth=1).info(f"\n report {report_name} created for user {user_id} with report_id {report_id}")
            else:
                logger.opt(depth=1).info(f"\nreport {report_name}_{report_id} creation failed with {create_report.status_code}")
        else:
            pass

        # upload call
        if upload_call:
            _unique_id = f"2ceb{random.randint(1000, 9999)}bahg54d{random.randint(100000, 999999)}a96"
            current_time = datetime.now(timezone.utc)

            _call_id = upload_call_to_imotio(
                token=token_for_user,
                unique_id=_unique_id,
                call_time=datetime(
                    current_time.year,
                    current_time.month,
                    current_time.day,
                    current_time.hour,
                    current_time.minute,
                    current_time.second
                ),
                filename='stereo.opus',
                client_phone='0987654321',
                operator_phone='1234567890',
                meta_data={'auto': 'test',
                           #'ID сотрудника': 123,
                           'upload': '',
                           # значение может быть пустым, это превратится в тег без значения
                           'communication_tag1': '1',
                           'communication_tag2': '',
                           'communication_tag3': '3',
                           'communication_tag4': '',
                           'communication_tag5': '5',
                           'communication_tag6': '',
                           'communication_tag7': '7',
                           'communication_tag8': '',
                           'communication_tag9': '9',
                           })

            if len(_call_id) == 24:
                logger.opt(depth=1).info(f"\n>>>>> AUDIO id: {_call_id} uploaded to {url} <<<<<")
            else:
                logger.opt(depth=1).info(f"\n>>>>> AUDIO upload error {_call_id} text  <<<<<")

            while True:
                start_time = time.time()
                check_is_processed = r.get(f"{url}/call/{_call_id}", headers=headers_for_user)
                check_is_processed.raise_for_status()  # выбросить исключение, если ошибка

                data = check_is_processed.json()
                is_processed = data.get("isProcessed", False)

                if is_processed:
                    logger.opt(depth=1).info(f"\n>>>>> AUDIO id: {_call_id} was processed <<<<<")
                    break

                if time.time() - start_time > 60:
                    logger.opt(depth=1).info(f"\n>>>>> AUDIO id: {_call_id} was not processed in 60 seconds <<<<<")
                    break

                time.sleep(3)
        else:
            pass

    return user_id, token, login


def create_operator(url: str, parent_user_id: str, password: str):

    name = login = f"auto_test_operator_{datetime.now().strftime('%m%d%H%M')}_{datetime.now().microsecond}"

    headers_for_get_token = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = {
        'username': '4adminIM',
        'password': 'Qaz123wsX'
    }

    get_token = r.post(f"{url}/token", headers=headers_for_get_token, data=data).json()
    token = f"Bearer {get_token['access_token']}"

    payload = {
        'role': 'operator',
        'login': login,
        'name': name,
        'password': password,
        'parentUser': parent_user_id
    }

    headers_for_create = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': token,
    }

    create = r.post(f"{url}/user", headers=headers_for_create, json=payload)
    user_id = create.text.replace('"', '')

    if create.status_code == 200:
        logger.opt(depth=1).info(f"\n>>>>> OPERATOR {name} WITH user_id: {user_id} CREATED SUCCESSFULLY <<<<<")
    else:
        logger.opt(depth=1).info(f"\n>>>>> ERROR CREATE OPERATOR {create.status_code} <<<<<")

    return user_id, token, login


def delete_user(url: str, token: str, user_id: str):

    headers_for_delete = {
        'accept': '*/*',
        'Authorization': token,
    }

    delete = r.delete(url=url + "/user/" + user_id, headers=headers_for_delete)

    if delete.status_code == 204:
        logger.opt(depth=1).info(f"\n>>>>> USER {user_id} DELETED <<<<<")
    else:
        logger.opt(depth=1).info(f"\n>>>>> USER {user_id} NOT DELETED <<<<<")


def give_users_to_manager(url: str, user_id_manager: str, user_id_users: list, token: str):

    headers_for_giving = {
        'accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        'Authorization': token,
    }
    #importFrom_id = '64b923905f95f6305573e619'
    #json_with_id = [USER_ID_USER, importFrom_id]

    give_user = r.put(f"{url}/user/{user_id_manager}/user_limitation", headers=headers_for_giving, json=user_id_users)

    if give_user.status_code == 204:
        logger.opt(depth=1).info(f"\n>>>>> USERS {user_id_users} GIVED TO MANAGER {user_id_manager} <<<<<")
    else:
        logger.opt(depth=1).info(f"\n>>>>> USERS {user_id_users} WAS NOT GIVED TO MANAGER {user_id_manager} <<<<<")


def give_manager_all_rights(url: str, user_id_manager: str, token: str):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        'Authorization': token,
    }
    json_with_rights = {'restt': 'true','delete_user': 'true', 'add_user': 'true','set_default_engine': 'true',
            'quota_edit': 'true', 'gpt_quota': 'true','user_modules_setup': 'true'}

    give_rights = r.put(f"{url}/user/{user_id_manager}/access_rights", headers=headers, json=json_with_rights)

    if give_rights.status_code == 204:
        logger.opt(depth=1).info(f"\n>>>>> MANAGER {user_id_manager} NOW HAVE ALL RIGHTS <<<<<")
    else:
        logger.opt(depth=1).info(f"\n>>>>> MANAGER {user_id_manager} FAILED TO GET ALL RIGHTS <<<<<")



def give_access_right(url: str, giver_token: str, recipient_id: str, access_right_list):
    """Admin can give for user and operator, user for operator"""

    headers_for_give = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': giver_token,
    }

    give_right = r.put(url=url + f'/user/{recipient_id}/access_rights',  headers=headers_for_give, json=access_right_list)

    if give_right.status_code == 204:
        logger.opt(depth=1).info(
            f"\n>>>>> FOR USER WITH user_id: {recipient_id} access_rights changed for {access_right_list} <<<<<")
    else:
        logger.opt(depth=1).info(
            f"\n>>>>> ERROR {give_right.status_code} changing access_rights FOR USER WITH user_id: {recipient_id} <<<<<")
