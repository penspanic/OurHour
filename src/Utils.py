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


def CreatePersonInfos(history: MessageHistory) -> List[PersonInfo]:
    personInfos = []
    # filter messages in history.messages by sender
    messagesBySender = {}
    for message in history.messages:
        if message.sender not in messagesBySender:
            messagesBySender[message.sender] = []
        messagesBySender[message.sender].append(message)

    for sender, messages in messagesBySender.items():
        personInfo = PersonInfo(sender, messages)
        personInfos.append(personInfo)

    return personInfos