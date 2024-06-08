import re
import datetime

from Messages import Message, MessageAttributes, MessageUtil

class MessageHistory:
    # static fields
    sunTalkThreshold = datetime.timedelta(days=1)


    def __init__(self):
        self.messages = []
        self.messagesByDate = {}
        self.lastReplyTimeBySender = {}
        self.messagesByMonth = {}

    def addMessage(self, message: Message):
        self.messages.append(message)
        dt = message.datetime.date()
        if dt not in self.messagesByDate:
            self.messagesByDate[dt] = []
        self.messagesByDate[dt].append(message)

        # get other sender name
        otherSender = None
        for sender in self.lastReplyTimeBySender.keys():
            if sender != message.sender:
                otherSender = sender
                break
        
        if otherSender is not None:
            message.replyTerm = message.datetime - self.lastReplyTimeBySender.get(otherSender, message.datetime)
            del self.lastReplyTimeBySender[otherSender]
        else:
            message.replyTerm = None

        self.lastReplyTimeBySender[message.sender] = message.datetime

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