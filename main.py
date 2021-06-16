import os
import re
import time

import requests
from rich.progress import Progress, TextColumn, BarColumn, TimeElapsedColumn, TimeRemainingColumn
from termcolor import colored

from prompt import PrintPrompt, print_hello
import cloud_music_apis.apis
import sims_analyzer
import plotly.graph_objects as go


def show_url(url):
    response = requests.get(url)

    file = open("caches/image.png", "wb")
    file.write(response.content)
    file.close()
    os.system('imgcat caches/image.png --height 10')


class Runner:
    top_function = ''
    obj_info = ''
    show_song_info_type = ''

    def __init__(self):
        os.system('clear')

    def run_c_m_e_a(self):
        prompt = PrintPrompt()
        while True:
            s = prompt.step
            res = prompt.print_prompt()
            if s == prompt.step:
                continue
            if prompt.step == -1:
                break

            if s == 0:
                self.top_function = res['top function']
                self.obj_info = res['info']
            elif s == 1:
                items = res['show items']
                if 'BACK TO UP MENU' in items:
                    continue
                user_info_dict = cloud_music_apis.apis.CloudMusicAPI().get_user_info(self.obj_info)
                user_name = user_info_dict['profile']['nickname']
                gender = cloud_music_apis.apis.format_gender(user_info_dict['profile']['gender'])
                creat_time = cloud_music_apis.apis.format_timestamp(user_info_dict['profile']['createTime'])
                last_active_time = cloud_music_apis.apis.format_timestamp(user_info_dict['userPoint']['updateTime'])
                online_status = user_info_dict['userPoint']['status']
                level = user_info_dict['level']
                balance = user_info_dict['userPoint']['balance']
                avatar_url = user_info_dict['profile']['avatarUrl']
                background_url = user_info_dict['profile']['backgroundUrl']
                listen_songs_num = user_info_dict['listenSongs']
                signature = user_info_dict['profile']['signature']
                if 'Avatar/Background Url' in items:
                    show_url(avatar_url)
                if 'User name' in items:
                    print('User name: ', user_name)
                if 'Gender' in items:
                    print('Gender: ', gender)
                if 'Level & Balance' in items:
                    print('Level: ', level)
                    print('Balance: ', balance)
                if 'Listen songs num' in items:
                    print('Listen songs num: ', listen_songs_num)
                if 'Avatar/Background Url' in items:
                    print('Avatar Url: ', avatar_url)
                    print('Background Url: ', background_url)
                if 'Signature' in items:
                    print('Signature: \n', signature)
                if 'Time infos(last active, account create time)' in items:
                    print('Account create time: ', creat_time)
                    print('Last active time: ', last_active_time)
                    if online_status == 1:
                        print('Online status: ', 'online')
                    else:
                        print('Online status: ', 'offline')
                name_score = sims_analyzer.analyze(user_name)
                signature_score = sims_analyzer.analyze(signature)
                score = 0
                if signature_score == 0:
                    score = name_score
                else:
                    score = (name_score * 0.6 + signature_score * 1.4) / 2
                print('User analyze: ',
                      sims_analyzer.judge_emotion(score, suffix='用户'),
                      '({}, {})'.format(name_score, signature_score))
                print()
            elif s == 2:
                obj_type = res['obj info type']
                if obj_type == 'NON':
                    continue
                self.show_song_info_type = obj_type
            elif s == 3:
                items = res['show items']
                if 'BACK TO UP MENU' in items:
                    continue
                song_list_info = cloud_music_apis.apis.CloudMusicAPI().get_playlist(self.obj_info)
                playlist = song_list_info['playlist']
                name = playlist['name']
                desc = playlist['description']
                tags = playlist['tags']
                tags_str = ' '.join(tags)
                print('Name: ', name)
                print('Create time: ', cloud_music_apis.apis.format_timestamp(playlist['createTime']))
                print('Last update time: ', cloud_music_apis.apis.format_timestamp(playlist['updateTime']))
                print('Description: ', desc)
                print('Tags: ', tags_str)
                tag_score = 0
                name_score = sims_analyzer.analyze(name)
                desc_score = sims_analyzer.analyze(desc)
                for tag in tags:
                    tag_score += sims_analyzer.analyze(tag)
                tag_score /= len(tags)
                print('Playlist analyze: ',
                      sims_analyzer.judge_emotion((name_score * 0.6 + desc_score * 1.4 + tag_score) / 3, suffix='歌单'),
                      '({}, {}, {})'.format(name_score, desc_score, tag_score))
            elif s == 4:
                lyric = cloud_music_apis.apis.CloudMusicAPI().get_song_lyric(self.obj_info)['tlyric']['lyric']
                if len(lyric) == 0:
                    lyric = cloud_music_apis.apis.CloudMusicAPI().get_song_lyric(self.obj_info)['lrc']['lyric']
                lyric = re.sub(r'\[.*?\]', '', lyric)
                lyric = re.sub(r'^\s*\n', '', lyric)

                lyric_list = lyric.split('\n')
                if os.path.exists('caches/lyrics.txt'):
                    with open('caches/lyrics.txt', "w") as file:
                        for content in lyric_list:
                            if len(content) == 0:
                                continue
                            score = sims_analyzer.analyze(content)
                            # print(content, sims_analyzer.judge_emotion(score), '{:5f}'.format(score))
                            file.write('{}\t{}\t{}\n\n'.format(content, sims_analyzer.judge_emotion(score, suffix='歌词'),
                                                               '{:5f}'.format(score)))
                    os.system('bat caches/lyrics.txt')
                os.system('clear')
                print_hello()
            elif s == 5:
                with Progress(TextColumn("[blue]{task.description}"),
                              BarColumn(bar_width=40),
                              "[progress.percentage]{task.percentage:>3.1f}%",
                              "•",
                              TimeElapsedColumn(),
                              "•",
                              TimeRemainingColumn(),
                              transient=True) as progress:
                    init_task_total = 100.0
                    if res['Terminal']:
                        init_task_total += 70.0
                    if res['Graph']:
                        init_task_total += 70.0
                    tid = progress.add_task('Getting initial comments info',
                                            start=True, total=init_task_total)
                    offset = res['offset']
                    limit = res['limit']
                    comments_dicts = []
                    if res['type'] == 'hot':
                        comments_dict = cloud_music_apis.apis.CloudMusicAPI().get_song_comment(self.obj_info,
                                                                                               True, offset, limit)
                        comment_type = 'hotComments'
                    else:
                        comments_dict = cloud_music_apis.apis.CloudMusicAPI().get_song_comment(self.obj_info,
                                                                                               False, offset, limit)
                        comment_type = 'comments'
                    total = comments_dict['total']
                    progress.update(tid, advance=50.0)

                    progress.update(tid, description='Correcting query params')
                    if total < int(offset) + int(limit):
                        if total < int(offset):
                            print(colored('Total: {}, overflowed'.format(total), 'red'))
                            continue
                        limit = str(total - int(offset))
                        print(colored('Total: {}, correction: limit: {}'.format(total, limit), 'red'))
                    time.sleep(1)

                    progress.update(tid, description='Getting all comments info', total=init_task_total+50.0)
                    limit_int = int(limit)
                    offset_int = int(offset)
                    count = 0
                    if limit_int < 100:
                        comments_dicts.append(comments_dict)
                    else:
                        while limit_int >= 0:
                            count += 1
                            now_limit = 100
                            if limit_int < 100:
                                now_limit = limit_int
                            if res['type'] == 'hot':
                                comments_dict = cloud_music_apis.apis.CloudMusicAPI().get_song_comment(
                                    self.obj_info, True, str(offset_int), str(now_limit))
                            else:
                                comments_dict = cloud_music_apis.apis.CloudMusicAPI().get_song_comment(
                                    self.obj_info, False, str(offset_int), str(now_limit))
                            comments_dicts.append(comments_dict)
                            limit_int -= 100
                            offset_int += 100

                    progress.update(tid, advance=50.0)

                    if res['Graph']:
                        progress.update(tid, description='Generate graph item', total=init_task_total + 20*count)
                        emotion_score = []
                        emotion_num = []
                        size = []
                        emotion_tag = []
                        for comments_dict in comments_dicts:
                            for comment in comments_dict[comment_type]:
                                content = comment['content']
                                score = sims_analyzer.analyze(content)
                                size.append((len(content) % 30) * 5)
                                score_short = round(score, 2)
                                if score_short in emotion_score:
                                    index = emotion_score.index(score_short)
                                    emotion_num[index] += 1
                                else:
                                    emotion_score.append(score_short)
                                    emotion_num.append(1)
                                    emotion_tag.append(sims_analyzer.judge_emotion(score, False))
                            progress.update(tid, advance=20.0)
                        fig = go.Figure(data=go.Scatter(
                            x=emotion_score,
                            y=emotion_num,
                            mode='markers',
                            marker=dict(size=size,
                                        color=emotion_score,
                                        showscale=True,
                                        ),
                            text=emotion_tag,
                            # hovertext=emotion_tag,
                        ))
                        fig.update_layout(title='Comments emotion analyze for song ' + self.obj_info)
                        progress.update(tid, dvance=50.0)
                        time.sleep(1)
                        fig.show()

                    if res['Terminal']:
                        if os.path.exists('caches/comments.txt'):
                            with open('caches/comments.txt', "w") as file:
                                progress.update(tid, description='Generate terminal item',
                                                total=init_task_total + 20 * count)
                                for comments_dict in comments_dicts:
                                    for comment in comments_dict[comment_type]:
                                        content = comment['content']
                                        score = sims_analyzer.analyze(content)
                                        # print(content, sims_analyzer.judge_emotion(score), '{:5f}'.format(score))
                                        file.write('{}\t{}\t{}\n\n'.format(content, sims_analyzer.judge_emotion(score),
                                                                           '{:5f}'.format(score)))
                                    progress.update(tid, advance=20.0)
                            progress.update(tid, dvance=50.0)
                            while not progress.finished:
                                progress.update(tid, advance=10.0)
                            time.sleep(1)
                            progress.stop()
                            time.sleep(1)
                            os.system('bat caches/comments.txt')
                    else:
                        pass
                    while not progress.finished:
                        progress.update(tid, advance=10.0)
                    progress.stop()
                    # if res['Terminal']:
                    #     os.system('bat caches/comments.txt')
                    os.system('clear')
                    print_hello()
            else:
                break


if __name__ == '__main__':
    runner = Runner()
    runner.run_c_m_e_a()
