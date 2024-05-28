from Messages import Message
import typing
import datetime

class PersonInfo:
    def __init__(self, name: str, messages: list):
        self.name = name
        self.messages = messages

        replyTerms = []
        for message in messages:
            if message.replyTerm is None:
                continue

            replyTerms.append(message.replyTerm)
        
        self.replyTermNormalized = sum(replyTerms, datetime.timedelta()) / len(replyTerms) if len(replyTerms) > 0 else None

class Comparison:
    def __init__(self, person1: PersonInfo, person2: PersonInfo):
        self.person1 = person1
        self.person2 = person2

        self.replyTermDiff = person1.replyTermNormalized - person2.replyTermNormalized if person1.replyTermNormalized is not None and person2.replyTermNormalized is not None else None

        # 비교 항목
        # 답장 텀(정규화)
        #  - 답장 텀 총합 / 메세지 개수