
from django.http import JsonResponse
from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt

from typing import Any, Callable
from urllib.parse import parse_qsl
import hashlib
import hmac
import json
from operator import itemgetter
import requests


def home(request):
    return render(request, 'telegramintegration/home.html')


@csrf_exempt
def sendData(request):
    data = request.POST
    username = data['username']
    password = data['password']
    data = safe_parse_webapp_init_data("5571212339:AAHxxYSJJcUnPTKBjE7UNyFxUxd5CYGoYhY", data["_auth"])
    text=   (f'Telegram username: {data["user"]["username"]}\n' + 
            f'Telegram id: {data["user"]["id"]}\n' +
            f'Telegram first name: {data["user"]["first_name"]}\n' +
            f'Telegram last name: {data["user"]["last_name"]}\n' +
            f'WebApp Username: {username}\n' + 
            f'WebApp Password: {password}')
    webhook = f'https://api.telegram.org/bot5571212339:AAHxxYSJJcUnPTKBjE7UNyFxUxd5CYGoYhY/sendMessage?chat_id={data["user"]["id"]}&text={text}'
    send_message(webhook)

    return JsonResponse({"ok": True, 'user': data['user']})

def send_message(webhook):
    return requests.post(webhook)

def check_webapp_signature(token: str, init_data: str) -> bool:
    try:
        parsed_data = dict(parse_qsl(init_data, strict_parsing=True))
    except ValueError: 
        return False
    if "hash" not in parsed_data:
        return False
    hash_ = parsed_data.pop("hash")

    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
    )
    secret_key = hmac.new(key=b"WebAppData", msg=token.encode(), digestmod=hashlib.sha256)
    calculated_hash = hmac.new(
        key=secret_key.digest(), msg=data_check_string.encode(), digestmod=hashlib.sha256
    ).hexdigest()
    return calculated_hash == hash_


def parse_webapp_init_data(init_data: str,*,loads: Callable[..., Any] = json.loads,):
    result = {}
    for key, value in parse_qsl(init_data):
        if (value.startswith("[") and value.endswith("]")) or (
                value.startswith("{") and value.endswith("}")
        ):
            value = loads(value)
        result[key] = value
    
    return result


def safe_parse_webapp_init_data(token: str,init_data: str,*,loads: Callable[..., Any] = json.loads,):
    if check_webapp_signature(token, init_data):
        return parse_webapp_init_data(init_data, loads=loads)
    raise ValueError("Invalid init data signature")