import requests
import pprint
from urllib.parse import quote
import base64
import json


if __name__ == '__main__':

    simulator = True #  FIX ME
    site = 'simulator-api.db.com' if simulator else 'api.db.com'
    redirect_uri = "" #  FIX ME
    redirect_uri_quote = quote(redirect_uri, safe='')
    client_id = "" if simulator else "" #  FIX ME
    if simulator:
        secret_key = "" #  FIX ME
    else:
        secret_key = "" #  FIX ME
    state = "" #  FIX ME
    IBAN = "" if simulator else '' #  FIX ME

    step = 1


    if step == 1:
        url1 = f"https://{site}/gw/oidc/authorize?response_type=code&redirect_uri={redirect_uri_quote}&client_id={client_id}&state={state}"
        print(url1)


    if step == 2:
        code = '' #  FIX ME

        base = base64.b64encode(f'{client_id}:{secret_key}'.encode("ascii"))
        headers2 = {
            "Authorization": f"Basic {base.decode('utf-8')}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data2 = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri
        }
        url2 = f"https://{site}/gw/oidc/token"
        answer3 = requests.post(url2, headers=headers2, data=data2)
        content = json.loads(answer3.content)

        print(content['access_token'])
        print(content['refresh_token'])

        # with open('content.json', 'w') as file:
        #     file.write(json.dumps(content))

    # with open('content.json', 'r') as file:
    #     content = json.loads(file.read())

    content = {
        "access_token": "", #  FIX ME
        "refresh_token": "" #  FIX ME
    }


    if step == 3:
        headers3 = {
            "accept": "application/json",
            "Authorization": f"Bearer {content['access_token']}"
        }
        url3 = f"https://{site}:443/gw/dbapi/banking/transactions/v2/"
        url3 += f"?iban={IBAN}&sortBy=bookingDate%5BDESC%5D&limit=20&offset=0"
        answer3 = requests.get(url3, headers=headers3)

        if answer3.status_code == 200:
            pprint.pprint(json.loads(answer3.text))
        else:
            print('refresh')


    if step == 4:
        refresh_url = f"https://{site}/gw/oidc/token"
        refresh_headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        refresh_data = {
            "grant_type": "refresh_token",
            "client_id": client_id,
            "client_secret": secret_key,
            "refresh_token": content['refresh_token']
        }
        refresh_answer = requests.post(refresh_url, headers=refresh_headers, data=refresh_data)
        new_content = json.loads(refresh_answer.content)

        headers4 = {
            "accept": "application/json",
            "Authorization": f"Bearer {new_content['access_token']}"
        }

        url4 = f"https://{site}:443/gw/dbapi/banking/transactions/v2/"
        url4 += f"?iban={IBAN}&sortBy=bookingDate%5BDESC%5D&limit=20&offset=0"
        answer4 = requests.get(url4, headers=headers4)

        if answer4.status_code == 200:
            pprint.pprint(json.loads(answer4.text))
        else:
            print('xz')
