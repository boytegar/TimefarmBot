import base64
import random
import socket
import requests
import urllib.parse
import json
import time
import subprocess
from datetime import datetime

# URL dan headers

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-ID,en-US;q=0.9,en;q=0.8,id;q=0.7',
    'content-length': '0',
    'priority': 'u=1, i',
    'Origin': 'https://tg-tap-miniapp.laborx.io',
    'Referer': 'https://tg-tap-miniapp.laborx.io/',
    'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
}

def load_credentials():
    # Membaca token dari file dan mengembalikan daftar token
    try:
        with open('query_id.txt', 'r') as f:
            queries = [line.strip() for line in f.readlines()]
        # print("Token berhasil dimuat.")
        return queries
    except FileNotFoundError:
        print("File query_id.txt tidak ditemukan.")
        return []
    except Exception as e:
        print("Terjadi kesalahan saat memuat token:", str(e))
        return []

def getuseragent(index):
    try:
        with open('useragent.txt', 'r') as f:
            useragent = [line.strip() for line in f.readlines()]
        if index < len(useragent):
            return useragent[index]
        else:
            return "Index out of range"
    except FileNotFoundError:
        return 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36'
    except Exception as e:
        return 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36'

def get_nama_from_init_data(init_data):
    parsed_data = urllib.parse.parse_qs(init_data)
    if 'user' in parsed_data:
        user_data = parsed_data['user'][0]
        data = ""
        user_data_json = urllib.parse.unquote(user_data)
        user_data_dict = json.loads(user_data_json)
        if 'first_name' in user_data_dict:
            data = user_data_dict['first_name']
        if 'last_name' in user_data_dict:
            data = data + " " + user_data_dict['last_name']
        if 'username' in user_data_dict:
            data = data + " " + f"({user_data_dict['username']})"
        return data
    return None

def auth(query, useragent):
    url = 'https://tg-bot-tap.laborx.io/api/v1/auth/validate-init/v2'
    headers['User-Agent'] = useragent
    payload = {
        'initData': query,
        'platform': 'android'
    }
    try:
        response_codes_done = range(200, 211)
        response_code_notfound = range(400, 410)
        response_code_failed = range(500, 530)
        response = requests.post(url, json=payload, headers=headers)
      
        if response.status_code in response_codes_done:
            return response.json()
        elif response.status_code in response_code_notfound:
            print(response.text)
            return None
        elif response.status_code in response_code_failed:
            return None
        else:
            raise Exception(f'Unexpected status code: {response.status_code}')
    except requests.exceptions.RequestException as e:
        print(f'Error making request: {e}')
        return None

def start_session(token, useragent):
    url = f'https://tg-bot-tap.laborx.io/api/v1/farming/start'
    headers['Authorization'] = f"Bearer {token}"
    headers['User-Agent'] = useragent
    try:
        response_codes_done = range(200, 211)
        response_code_notfound = range(400, 410)
        response_code_failed = range(500, 530)
        response = requests.post(url, json={}, headers=headers)
      
        if response.status_code in response_codes_done:
            return response.json()
        elif response.status_code in response_code_notfound:
            error = response.json().get('error')
            print(f"{error.get('message')}")
            return None
        elif response.status_code in response_code_failed:
            return None
        else:
            raise Exception(f'Unexpected status code: {response.status_code}')
    except requests.exceptions.RequestException as e:
        print(f'Error making request: {e}')
        return None

def claim_session(token, useragent):
    url = f'https://tg-bot-tap.laborx.io/api/v1/farming/finish'
    headers['Authorization'] = f"Bearer {token}"
    headers['User-Agent'] = useragent
    try:
        response_codes_done = range(200, 211)
        response_code_notfound = range(400, 410)
        response_code_failed = range(500, 530)
        response = requests.post(url, json={}, headers=headers)
      
        if response.status_code in response_codes_done:
            return response.json()
        elif response.status_code in response_code_notfound:
            error = response.json().get('error')
            print(f"{error.get('message')}")
            return None
        elif response.status_code in response_code_failed:
            return None
        else:
            raise Exception(f'Unexpected status code: {response.status_code}')
    except requests.exceptions.RequestException as e:
        print(f'Error making request: {e}')
        return None

def claim_ref(token, useragent):
    url = f"https://tg-bot-tap.laborx.io/api/v1/balance/referral/claim"
    headers['Authorization'] = f"Bearer {token}"
    headers['User-Agent'] = useragent
    try:
        response_codes_done = range(200, 211)
        response_code_notfound = range(400, 410)
        response_code_failed = range(500, 530)
        response = requests.post(url, {}, headers=headers)
      
        if response.status_code in response_codes_done:
            return response.json()
        elif response.status_code in response_code_notfound:
            error = response.json().get('error')
            print(f"Ref status : {error.get('message')}")
            return None
        elif response.status_code in response_code_failed:
            return None
        else:
            raise Exception(f'Unexpected status code: {response.status_code}')
    except requests.exceptions.RequestException as e:
        print(f'Error making request: {e}')
        return None

def get_list_quest(token, useragent):
    url = f"https://tg-bot-tap.laborx.io/api/v1/tasks"
    headers['Authorization'] = f"Bearer {token}"
    headers['User-Agent'] = useragent
    try:
        response_codes_done = range(200, 211)
        response_code_notfound = range(400, 410)
        response_code_failed = range(500, 530)
        response = requests.get(url, headers=headers)
      
        if response.status_code in response_codes_done:
            return response.json()
        elif response.status_code in response_code_notfound:
            print(response.text)
            return None
        elif response.status_code in response_code_failed:
            return None
        else:
            raise Exception(f'Unexpected status code: {response.status_code}')
    except requests.exceptions.RequestException as e:
        print(f'Error making request: {e}')
        return None

def sumbit_submission(token, id, useragent):
    url = f"https://tg-bot-tap.laborx.io/api/v1/tasks/{id}/submissions"
    headers['Authorization'] = f"Bearer {token}"
    headers['User-Agent'] = useragent
    try:
        response_codes_done = range(200, 211)
        response_code_notfound = range(400, 410)
        response_code_failed = range(500, 530)
        response = requests.post(url, json={}, headers=headers)
      
        if response.status_code in response_codes_done:
            return response.json()
        elif response.status_code in response_code_notfound:
            return None
        elif response.status_code in response_code_failed:
            return None
        else:
            raise Exception(f'Unexpected status code: {response.status_code}')
    except requests.exceptions.RequestException as e:
        print(f'Error making request: {e}')
        return None

def submitted(token, id, useragent):
    url = f'https://tg-bot-tap.laborx.io/api/v1/tasks/{id}'
    headers['Authorization'] = f"Bearer {token}"
    headers['User-Agent'] = useragent
    try:
        response_codes_done = range(200, 211)
        response_code_notfound = range(400, 410)
        response_code_failed = range(500, 530)
        response = requests.get(url, headers=headers)
      
        if response.status_code in response_codes_done:
            return response.json()
        elif response.status_code in response_code_notfound:
            return None
        elif response.status_code in response_code_failed:
            return None
        else:
            raise Exception(f'Unexpected status code: {response.status_code}')
    except requests.exceptions.RequestException as e:
        print(f'Error making request: {e}')
        return None

def claims(token, id, useragent):
    url = f"https://tg-bot-tap.laborx.io/api/v1/tasks/{id}/claims"
    headers['Authorization'] = f"Bearer {token}"
    headers['User-Agent'] = useragent
    try:
        response_codes_done = range(200, 211)
        response_code_notfound = range(400, 410)
        response_code_failed = range(500, 530)
        response = requests.post(url, {}, headers=headers)
      
        if response.status_code in response_codes_done:
            return response.json()
        elif response.status_code in response_code_notfound:
            print(response.json())
            return None
        elif response.status_code in response_code_failed:
            return None
        else:
            raise Exception(f'Unexpected status code: {response.status_code}')
    except requests.exceptions.RequestException as e:
        print(f'Error making request: {e}')
        return None

def upgraded(token, useragent):
    url = 'https://tg-bot-tap.laborx.io/api/v1/me/level/upgrade'
    headers['Authorization'] = f"Bearer {token}"
    headers['User-Agent'] = useragent
    try:
        response_codes_done = range(200, 211)
        response_code_notfound = range(400, 410)
        response_code_failed = range(500, 530)
        response = requests.post(url, json={}, headers=headers)
      
        if response.status_code in response_codes_done:
            return response.json()
        elif response.status_code in response_code_notfound:
            print(response.text)
            return None
        elif response.status_code in response_code_failed:
            return None
        else:
            raise Exception(f'Unexpected status code: {response.status_code}')
    except requests.exceptions.RequestException as e:
        print(f'Error making request: {e}')
        return None

# Main program

def mainclaim():

    while True:
        selector_ref = input("Claim ref point ? (default n) (y/n): ").strip().lower()
        if selector_ref in ['y', 'n', '']:
            selector_ref = selector_ref or 'n'
            break
        else:
            print("Input 'y' or 'n'.")

    while True:
        auto_upgrade = input("Auto upgrade boost ? (default n) (y/n): ").strip().lower()
        if auto_upgrade in ['y', 'n', '']:
            auto_upgrade = auto_upgrade or 'n'
            break
        else:
            print("Input 'y' or 'n'.")
    
    while True:
        queries = load_credentials()
        for index, query in enumerate(queries):
            useragent = getuseragent(index)
            data_auth = auth(query, useragent)
            if data_auth is not None:
                token = data_auth.get('token')
                info = data_auth.get('info')
                level = info.get('level')
                balanceInfo = data_auth.get('balanceInfo')
                balance = balanceInfo.get('balance')
                levelDesc = data_auth.get('levelDescriptions')
                nama = get_nama_from_init_data(query)
                print(f"===== Name : {nama} || Balance : {balance} =====")

                if auto_upgrade == 'y':
                    for lev in levelDesc:
                        if int(lev.get('level')) == level+1:
                            print("upgarded....")
                            time.sleep(3)
                            if balance < lev.get('price'):
                                print('Not Enough Balance')
                            else:
                                upgr = upgraded(token, useragent)
                                if upgr is not None:
                                    print(f"Success upgrade to : {upgr.get('level')}")
                                    print(f"Available Balance : {upgr.get('balance')}")

                
                daily_response = claim_session(token, useragent)
                if daily_response is not None:
                    print("Claimed Done")
                time.sleep(3)

                start_response = start_session(token, useragent)
                if start_response is not None:
                    print("Mine Started")
                time.sleep(3)

                if selector_ref == 'y':
                    claim_ref_response = claim_ref(token, useragent)
                    if claim_ref_response is not None:
                        print("Claim Ref success")
                    time.sleep(3)

            else:
                print("Auth Failed")
            time.sleep(5)
            print()
        
        times = random.randint(14400, 14600)
        printdelay(times)
        time.sleep(times)

def maintask():
    queries = load_credentials()
    for index, query in enumerate(queries):
        nama = get_nama_from_init_data(query)
        print(nama)
        useragent = getuseragent(index)
        data_auth = auth(query, useragent)
        if data_auth is not None:
            token = data_auth.get('token')
            list_quest = get_list_quest(token, useragent)
            if list_quest is not None:
                for quest in list_quest:
                    submission = sumbit_submission(token, quest.get('id'), useragent)
                    if submission is not None:
                        time.sleep(2)
                        print("submission start")
                    else:
                        print("submission Done")
                        time.sleep(2)
                    
                    submit = submitted(token, quest.get('id'), useragent)
                    print(submit)
                    if submit is not None:
                        time.sleep(2)
                        print("submit start")
                    else:
                        print("submit Done")
                        time.sleep(2)

                    data_claims = claims(token, quest.get('id'), useragent)
                    print(data_claims)
                    if data_claims is not None:
                        print(f"task {quest.get('id')} claims success")
                    else:
                        print("failed claims")
        else:
            print("auth error")
        

################################################################################################################################################################
################################################################################################################################################################
################################################################################################################################################################

def main():
    print(r"""\n        \n            Created By Snail S4NS Group\n    find new airdrop & bot here: t.me/sanscryptox\n              \n        select this one :\n        1. claim daily every 4 hours\n        2. claim all task(soon)\n          \n          """)

    selector = input("Select the one ? (default 1): ").strip().lower()

    if selector == '1':
        mainclaim()
    elif selector == '2':
        exit()
    else:
        exit()

def printdelay(delay):
    now = datetime.now().isoformat(" ").split(".")[0]
    hours, remainder = divmod(delay, 3600)
    minutes, sec = divmod(remainder, 60)
    print(f"{now} | Waiting Time: {hours} hours, {minutes} minutes, and {sec} seconds")

def print_welcome_message(serial=None):
    print(r"""\n              \n            Created By Snail S4NS Group\n    find new airdrop & bot here: t.me/sansxgroup\n              \n          """)
    print()
    if serial is not None:
        print(f"Copy, tag bot @SnailHelperBot and paste this key in discussion group t.me/sansxgroup")
        print(f"Your key : {serial}")

def read_serial_from_file(filename):
    serial_list = []
    with open(filename, 'r') as file:
        for line in file:
            serial_list.append(line.strip())
    return serial_list

serial_file = "serial.txt"
serial_list = read_serial_from_file(serial_file)

def get_serial(current_date, getpcname, name, status):
    formatted_current_date = current_date.strftime("%d-%m-%Y")
    # Encode each value using base64
    getpcname += "knjt"
    name    += "knjt"
    encoded_getpcname = base64.b64encode(getpcname.encode()).decode().replace("=", "")
    encoded_current_date = base64.b64encode(formatted_current_date.encode()).decode().replace("=", "")
    encoded_name = base64.b64encode(name.encode()).decode().replace("=", "")
    encoded_status = base64.b64encode(str(status).encode()).decode().replace("=", "")

    # Calculate the length of each encoded value
    getpcname_len = len(encoded_getpcname)
    current_date_len = len(encoded_current_date)
    name_len = len(encoded_name)
    status_len = len(encoded_status)

    # Concatenate the encoded values with their lengths
    serial = "S4NS-"
    serial += str(getpcname_len).zfill(2) + encoded_getpcname
    serial += str(current_date_len).zfill(2) + encoded_current_date
    serial += str(name_len).zfill(2) + encoded_name
    serial += str(status_len).zfill(2) + encoded_status
    return serial

def decode_pc(serial, getpcname, name, current_date):
    try:
        getpcname_len = int(serial[5:7])
        encoded_getpcname = serial[7:7+getpcname_len]
        current_date_len = int(serial[7+getpcname_len:9+getpcname_len])
        encoded_current_date = serial[9+getpcname_len:9+getpcname_len+current_date_len]
        name_len = int(serial[9+getpcname_len+current_date_len:11+getpcname_len+current_date_len])
        encoded_name = serial[11+getpcname_len+current_date_len:11+getpcname_len+current_date_len+name_len]
        status_len = int(serial[11+getpcname_len+current_date
