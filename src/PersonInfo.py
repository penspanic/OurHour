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
        #print(f'replyTermNormalized = {termSum} / {termCount if termCount > 0 else None}')
        self.replyTermNormalized = termSum / termCount if termCount > 0 else None
        self.averageMessageLength = sum([len(message.getMessage()) for message in messages]) / len(messages) if len(messages) > 0 else None
        self.giftSentCount = len([message for message in messages if Messages.MessageAttributes.gift in message.attributes])
        self.sunTalkCount = len([message for message in messages if Messages.MessageAttributes.suntalk in message.attributes])
        self.emoticonMessageCount = len([message for message in messages if Messages.MessageAttributes.emoticon in message.attributes])

    def print(self):
        print()
        print(self.name)
        print(f'replyTermNormalized: {Utils.formatTimeDelta(self.replyTermNormalized)}')
        print(f'averageMessageLength: {self.averageMessageLength}')
        print(f'giftSentCount: {self.giftSentCount}')
        print(f'sunTalkCount: {self.sunTalkCount}')
        print(f'emoticonRatio: {self.emoticonRatio}')

    def asDict(self):
        return {
            '이름': self.name,
            '평균 답장 텀': Utils.formatTimeDelta(self.replyTermNormalized),
            '평균 메세지 길이': self.averageMessageLength,
            '선물 횟수': self.giftSentCount,
            '선톡 횟수': self.sunTalkCount,
            '이모티콘 비율(%)': f"{(self.emoticonMessageCount / len(self.messages) if len(self.messages) > 0 else 0) * 100:.2f}",
            '메세지 수': len(self.messages),
            '이모티콘 수': self.emoticonMessageCount,
        }