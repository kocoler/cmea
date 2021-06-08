import hashlib
import json
from datetime import datetime

import requests
from . import encrypt_params
from urllib.parse import urlencode


class CloudMusicAPI:
    cookie_init = dict(os='pc')
    cookie_jar = cookie_init

    def __init__(self):
        self.headers = {
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
            'Origin': 'https://music.163.com',
            'Referer': 'https://music.163.com/',
            'Host': 'music.163.com',
            'Nm-GCore-Status': '1',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/90.0.4430.212 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'NMTID=00O30M12b0uXhmlo0VFhevxtchLWe0AAAF5bjFdiw'
        }
        self.json_headers = {
            'Origin': 'https://music.163.com',
            'Referer': 'https://music.163.com/',
            'Host': 'music.163.com',
            'Nm-GCore-Status': '1',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/90.0.4430.212 Safari/537.36',
            'Content-Type': 'application/json',
        }

    def login(self, username, password) -> dict:
        url = "https://music.163.com/weapi/login"

        params = encrypt_params.generate_encrypt_params(
            {
                'username': username,
                'password': hashlib.md5(bytes(password, encoding="utf-8")).hexdigest(),
                'rememberLogin': 'true',
            }
        )
        payload = urlencode(params)

        response = requests.request("POST", url, headers=self.headers, data=payload, cookies=self.cookie_init)
        self.cookie_jar = response.cookies
        return json.loads(response.text)

    def get_user_pre_comment(self):
        pass

    def get_user_playlist(self, uid, limit='100', offset='0') -> dict:
        url = "https://music.163.com/weapi/user/playlist?csrf_token="

        params = encrypt_params.generate_encrypt_params(
            {
                "offset": offset,
                "uid": uid,
                "limit": limit,
                "csrf_token": ""
            }
        )
        # cebdbac
        # cac c e a
        # ecd c e a
        # dca c e a/d
        # aba c e d a
        # bac c e d a b
        # cedab a b c d e
        payload = urlencode(params)

        response = requests.request("POST", url, headers=self.headers, data=payload)
        return json.loads(response.text)

    def get_playlist(self, id, offset='0', total=False, n=20, limit=20) -> dict:
        url = "https://music.163.com/weapi/v3/playlist/detail"

        params = encrypt_params.generate_encrypt_params(
            {
                "id": id,
                "offset": offset,
                "total": total,
                "n": limit,
                "limit": limit,
                "csrf_token": ""
            }
        )
        payload = urlencode(params)

        response = requests.request("POST", url, headers=self.headers, data=payload)
        return json.loads(response.text)

    def get_songs_info(self, ids, offset='0', total=False, n=20, limit=20) -> dict:
        url = "https://music.163.com/weapi/v3/playlist/detail"

        params = encrypt_params.generate_encrypt_params(
            {
                'c': json.dumps([
                    {
                        'id': ids[0]
                    },
                    {
                        'id': ids[1]
                    }
                ]),
                "ids": json.dumps(ids),
                "csrf_token": ""
            }
        )
        payload = urlencode(params)

        response = requests.request("POST", url, headers=self.headers, data=payload)
        return json.loads(response.text)

    def get_user_info(self, uid) -> dict:
        url = "https://music.163.com/api/v1/user/detail/" + uid

        params = encrypt_params.generate_encrypt_params(
            {
                "csrf_token": ""
            }
        )
        payload = urlencode(params)

        response = requests.request("GET", url, headers=self.headers, data=payload)
        return json.loads(response.text)

    def get_song_lyric(self, id) -> dict:
        url = "https://music.163.com/api/song/lyric?os=osx&id=" + id + '&lv=-1&kv=-1&tv=-1'

        response = requests.request("GET", url, headers=self.json_headers)
        return json.loads(response.text)

    def get_song_comment(self, id, hot=False, offset='0', limit='30') -> dict:
        hot_query = "hotcomments"
        if not hot:
            hot_query = "comments"

        url = "http://music.163.com/weapi/v1/resource/" + hot_query + "/R_SO_4_" + str(id)

        params = encrypt_params.generate_encrypt_params(
            {
                "rid": 'R_SO_4_' + str(id),
                "offset": offset,
                "limit": limit,
                "total": False,
                "csrf_token": ""
            }
        )
        payload = urlencode(params)

        response = requests.request("POST", url, headers=self.headers, data=payload)
        comments = response.text
        comments_dict = json.loads(comments)
        # print(response.text)
        return comments_dict


def format_gender(gender) -> str:
    if gender == 1:
        return '男'
    elif gender == 2:
        return '女'
    else:
        return '未知'


def format_timestamp(timestamp) -> str:
    return str(datetime.fromtimestamp(timestamp/1000))

