from typing import List
from MessageHistory import MessageHistory
from PersonInfo import PersonInfo


def createPersonInfos(history: MessageHistory) -> List[PersonInfo]:
    personInfos = []
    for name in history.messagesBySender.keys():
        personInfos.append(createPersonInfo(history, name))

    return personInfos

def createPersonInfo(history: MessageHistory, name: str) -> PersonInfo:
    messages = [message for message in history.messages if message.sender == name]
    return PersonInfo(name, messages)