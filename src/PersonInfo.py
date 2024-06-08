import Messages
from typing import List
import datetime
import Utils

class PersonInfo:
    def __init__(self, name: str, messages: List[Messages.Message]):
        self.name = name
        self.messages = messages

        replyTerms = [] # type: List[datetime.timedelta]
        for message in messages:
            if message.replyTerm is None:
                continue

            replyTerms.append(message.replyTerm)

        termSum = datetime.timedelta()
        for term in replyTerms:
            termSum += term

        termCount = len(replyTerms)
        print(f'replyTermNormalized = {termSum} / {termCount if termCount > 0 else None}')
        self.replyTermNormalized = termSum / termCount if termCount > 0 else None
        self.AverageMessageLength = sum([len(message.getMessage()) for message in messages]) / len(messages) if len(messages) > 0 else None
        self.giftSentCount = len([message for message in messages if Messages.MessageUtil.IsGift(message)])

    def print(self):
        print()
        print(self.name)
        print(f'replyTermNormalized: {Utils.formatTimeDelta(self.replyTermNormalized)}')
        print(f'AverageMessageLength: {self.AverageMessageLength}')
        print(f'giftSentCount: {self.giftSentCount}')


class Comparison:
    def __init__(self, person1: PersonInfo, person2: PersonInfo):
        self.person1 = person1
        self.person2 = person2

        self.replyTermDiff = person1.replyTermNormalized - person2.replyTermNormalized if person1.replyTermNormalized is not None and person2.replyTermNormalized is not None else None

        # 비교 항목
        # 답장 텀(정규화)
        #  - 답장 텀 총합 / 메세지 개수