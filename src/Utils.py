from datetime import timedelta
from typing import List
from PersonInfo import PersonInfo
from MessageHistory import *

def formatTimeDelta(delta: timedelta) -> str:
    total_seconds = int(delta.total_seconds())

    days, remainder = divmod(total_seconds, 24 * 3600)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    return f'{days}d {hours}h {minutes}m {seconds}s'


def createPersonInfos(history: MessageHistory) -> List[PersonInfo]:
    personInfos = []
    for name in history.messagesBySender.keys():
        personInfos.append(createPersonInfo(history, name))

    return personInfos

def createPersonInfo(history: MessageHistory, name: str) -> PersonInfo:
    messages = [message for message in history.messages if message.sender == name]
    return PersonInfo(name, messages)