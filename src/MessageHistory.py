import re

from Messages import Message, MessageAttributes, MessageUtil

class MessageHistory:
    def __init__(self):
        self.messages = []
        self.messagesByDate = {}
        self.lastReplyTimeBySender = {}

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

        if MessageUtil.IsGift(message):
            message.attributes.add(MessageAttributes.gift)

        if MessageUtil.IsEmoticon(message):
            message.attributes.add(MessageAttributes.emoticon)

    def __str__(self):
        return '\n'.join([str(message) for message in self.messages])

    def __repr__(self):
        return '\n'.join([str(message) for message in self.messages])


