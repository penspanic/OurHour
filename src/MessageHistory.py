import re
import datetime

from Messages import Message, MessageAttributes, MessageUtil

class MessageHistory:
    # static fields
    sunTalkThreshold = datetime.timedelta(days=1)
    replyTermThreshold = datetime.timedelta(days=5)


    def __init__(self):
        self.messages = []
        self.messagesByDate = {}
        self.messagesBySender = {}
        self.messagesByMonth = {}

    def addMessage(self, message: Message):

        self.messages.append(message)
        dt = message.datetime.date()
        if dt not in self.messagesByDate:
            self.messagesByDate[dt] = []
        self.messagesByDate[dt].append(message)

        if message.sender not in self.messagesBySender:
            self.messagesBySender[message.sender] = []
        self.messagesBySender[message.sender].append(message)


        # 답장 텀:
        # 상대방이 보낸 메세지 다음에 내가 메세지를 보냄, 그 사이 걸린 시간
        # 만약 이전 메세지가 내 메세지라면, 답장 텀으로 인식하지 않음
        lastMessage = self.messages[-2] if len(self.messages) >= 2 else None
        if lastMessage is not None and lastMessage.sender != message.sender:
            message.replyTerm = message.datetime - lastMessage.datetime
            if message.replyTerm > MessageHistory.replyTermThreshold:
                message.replyTerm = None


        # messages by month
        month = message.datetime.replace(day=1)
        if month not in self.messagesByMonth:
            self.messagesByMonth[month] = []
        self.messagesByMonth[month].append(message)

        if MessageUtil.IsGift(message):
            message.attributes.add(MessageAttributes.gift)

        if MessageUtil.IsEmoticon(message):
            message.attributes.add(MessageAttributes.emoticon)

        if MessageUtil.IsSunTalk(message, self.messagesByDate[dt], MessageHistory.sunTalkThreshold):
            message.attributes.add(MessageAttributes.suntalk)

    def __str__(self):
        return '\n'.join([str(message) for message in self.messages])

    def __repr__(self):
        return '\n'.join([str(message) for message in self.messages])