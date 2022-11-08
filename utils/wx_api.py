import requests

from django.conf import settings


def code2session(js_code):
    url = "https://api.weixin.qq.com/sns/jscode2session"
    payload = {
        "appid": settings.APPID,
        "secret": settings.APP_SECRET,
        "js_code": js_code,
        "grant_type": "authorization_code"
    }
    response = requests.get(url, params=payload)
    return response.json()
