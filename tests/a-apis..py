import json
import re

import requests
import encrypt_params
from urllib.parse import urlencode


class CloudMusicAPI:
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
        print(response.text)
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
        print(response.text)
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
        print(response.text)
        return comments_dict

# get_user_playlist('130812247', '100', '0')
CloudMusicAPI().get_playlist("811456267")
# get_songs_info([34367063, 2529472])
# get_user_info("130812247")
# get_song_lyric("869158")
# CloudMusicAPI().get_song_comment("513256641", False)

# lyric = CloudMusicAPI().get_song_lyric("4930076")['tlyric']['lyric']
# print(len(lyric))
# res = re.sub(r'\[.*?\]', '', lyric)
# res = re.sub(r'^\s*\n', '', res)
# print(res)


