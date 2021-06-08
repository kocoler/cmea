from snownlp import SnowNLP
from termcolor import colored


def analyze(words) -> float:
    return SnowNLP(words).sentiments


def judge_emotion(score, color=True, suffix='评论') -> str:
    if score >= 0.9:
        if color:
            return colored('极喜/极激动/舒服的'+suffix, 'red', attrs=['bold'])
        return '极喜/极激动/舒服的评论'
    elif score >= 0.8:
        if color:
            return colored('带有喜/激动的'+suffix, 'red')
        return '带有喜/激动的'+suffix
    elif score >= 0.7:
        if color:
            return colored('带有开心/乐观的'+suffix, 'green')
        return '带有开心/乐观的'+suffix
    elif score >= 0.6:
        if color:
            return colored('带有喜的成分的'+suffix, 'yellow')
        return '带有喜的成分的'+suffix
    elif score >= 0.5:
        if color:
            return colored('一般平静/正常的'+suffix, 'magenta')
        return '一般平静/正常的'+suffix
    elif score >= 0.4:
        if color:
            return colored('稍有消极/负面的'+suffix, 'cyan')
        return '稍有消极/负面的'+suffix
    elif score >= 0.3:
        if color:
            return colored('带有悲/生气的'+suffix, 'yellow')
        return '带有悲/生气的'+suffix
    elif score >= 0.2:
        if color:
            return colored('带有消极/负面/生气的'+suffix, 'grey')
        return '带有消极/负面/生气的'+suffix
    elif score >= 0.1:
        if color:
            return colored('极消极/极负面/极悲的'+suffix, 'red')
        return '极消极/极负面/极悲的'+suffix
    else:
        if color:
            return colored('来自地狱的'+suffix, 'red', attrs=['bold'])
        return '来自地狱的'+suffix


