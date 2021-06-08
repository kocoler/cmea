from __future__ import print_function, unicode_literals
from pyfiglet import Figlet
from PyInquirer import prompt, Separator
from termcolor import colored


def print_hello():
    f = Figlet(font='slant')
    print(f.renderText("C M E A"))
    print(colored("Cloud Music Emotion Analyzer\n", 'red'))


def print_bey():
    f = Figlet(font='block')
    print(f.renderText("B E Y"))


def get_function_obj(answers) -> str:
    obj_str = answers['top function']
    if obj_str == 'Functions related to users':
        return 'Input user name'
    elif obj_str == 'Functions related to songs':
        return 'Input songs name'
    elif obj_str == 'Functions related to playlist':
        return 'Input user playlist name'

    return 'QUIT'


def print_menu_level_1() -> dict:
    questions = [
        {
            'type': 'list',
            'name': 'top function',
            'message': 'Welcome to CMEA(cloud music emotion analyzer)! What do you want to do?',
            'choices': [
                'Functions related to users',
                'Functions related to songs',
                'Functions related to playlist',
                Separator(),
                'ALREADY TOP MENU LEVEL, CLICK TO QUIT'
            ]
        },
        {
            'type': 'input',
            'name': 'obj info',
            'message': 'Input your function obj info:',
        }
    ]
    answers = prompt(questions)
    return answers


def print_menu_song_info() -> dict:
    questions = [
        {
            'type': 'list',
            'name': 'obj info type',
            'message': 'Which do you want to see?',
            'choices': [
                'Show song info',
                'Show comments',
                Separator(),
                'BACK TO UP MENU'
            ]
        }
    ]
    answers = prompt(questions)
    return answers


def print_comments_level_1() -> dict:
    questions = [
        {
            'type': 'checkbox',
            'name': 'comment type',
            'message': 'Which comment type do you want to see?',
            'choices': [
                Separator('= Comments type ='),
                {'name': 'Hot comments', 'checked': True},
                {'name': 'Normal comments'},
                Separator('= Shows type ='),
                {'name': 'Terminal', 'checked': False},
                {'name': 'Graph'},
                # Separator('= Others ='),
                # {'name': 'BACK TO UP MENU'}
            ],
            'validate': lambda answer: 'You must choose one comments type.' \
                if len(answer) != 1 else True
        },
        {
            'type': 'input',
            'name': 'offset',
            'message': 'Input comments offset:',
        },
        {
            'type': 'input',
            'name': 'limit',
            'message': 'Input comments limit:',
        },
    ]
    answers = prompt(questions)
    return answers


def print_user_info():
    questions = [
        {
            'type': 'checkbox',
            'name': 'show items',
            'message': 'Which user information do you want to see?',
            'choices': [
                Separator('= Basic info ='),
                {'name': 'User name', 'checked': True},
                {'name': 'Gender'},
                {'name': "Level & Balance"},
                {'name': 'Listen songs num'},
                {'name': 'Avatar/Background Url'},
                {'name': 'Signature'},
                Separator('= Advanced info ='),
                {'name': 'Time infos(last active, account create time)'},
                {'name': 'User emotion analyze', 'disabled': 'default, must be chosen'},
                {'name': 'More info ...', 'disabled': 'not implemented'},
                Separator('= Others ='),
                {'name': 'BACK TO UP MENU'}
            ],
            'validate': lambda answer: 'You must choose at least one topping.' \
                if len(answer) == 0 else True
        }
    ]
    answers = prompt(questions)
    return answers


def print_song_list():
    questions = [
        {
            'type': 'checkbox',
            'name': 'show items',
            'message': 'Which playlist information do you want to see?',
            'choices': [
                Separator('= Basic info ='),
                {'name': 'Basic info and playlist emotion analyze', 'checked': True},
                {'name': 'More info ...', 'disabled': 'not implemented'},
                Separator('= Others ='),
                {'name': 'BACK TO UP MENU'}
            ],
            'validate': lambda answer: 'You must choose at least one topping.' \
                if len(answer) == 0 else True
        }
    ]
    answers = prompt(questions)
    return answers


class PrintPrompt:
    steps = {"menu_hello": 0, "menu_show_user_info": 1, "menu_show_song": 2, "menu_show_song_list": 3,
             "menu_show_song_info": 4,
             "menu_show_comment_info": 5}
    step = 0

    def __init__(self):
        self.step = 0
        print_hello()

    def print_prompt(self) -> dict:
        s = self.step
        if s == 0:
            answers = print_menu_level_1()
            obj_str = answers['top function']
            if obj_str == 'Functions related to users':
                answers['top function'] = 'user'
            elif obj_str == 'Functions related to songs':
                answers['top function'] = 'songs'
            elif obj_str == 'Functions related to playlist':
                answers['top function'] = 'playlist'
            else:
                answers['top function'] = 'quit'

            if answers['top function'] == 'user':
                self.step = 1
            elif answers['top function'] == 'songs':
                self.step = 2
            elif answers['top function'] == 'playlist':
                self.step = 3
            else:
                print_bey()
                self.step = -1

            return {"top function": answers['top function'], "info": answers['obj info']}
        elif s == 1:
            answers = print_user_info()
            self.step = 0
            return answers
        elif s == 2:
            answers = print_menu_song_info()
            if answers['obj info type'] == 'Show song info':
                self.step = 4
                answers['obj info type'] = 'song'
            elif answers['obj info type'] == 'Show comments':
                self.step = 5
                answers['obj info type'] = 'comments'
            else:
                answers['obj info type'] = 'NON'
                self.step = 0
            return answers
        elif s == 3:
            answers = print_song_list()
            self.step = 0
            return answers
        elif s == 4:
            self.step = 2
        elif s == 5:
            self.step = 2
            answers = print_comments_level_1()
            res = {'Terminal': False, 'Graph': False, 'offset': answers['offset'], 'limit': answers['limit']}
            if answers['comment type'][0] == 'Hot comments':
                res['type'] = 'hot'
            else:
                res['type'] = 'normal'
            for i in answers['comment type']:
                if i == 'Terminal':
                    res['Terminal'] = True
                if i == 'Graph':
                    res['Graph'] = True
            return res
