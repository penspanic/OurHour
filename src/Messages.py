import datetime
import re

class MessageAttributes:
    gift = 'gift'
    emoticon = 'emoticon'

class Message:
    def __init__(self, sender: str, datetime: datetime.datetime, messageLines: str):
        self.sender = sender
        self.datetime = datetime
        self.messageLines = messageLines
        self.attributes = set()
        self.replyTerm = None # datetime.timedelta
    
    def getMessage(self):
        return '\n'.join(self.messageLines)

    def __str__(self):
        s = f'{self.sender} {self.datetime}'
        if self.replyTerm is not None:
            s += f' term:({self.replyTerm})'
        s += f' {self.getMessage()}'
        return s

    def __repr__(self):
        return f'{self.sender} {self.datetime} {self.getMessage()}'
    
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


class MessageUtil:
    giftPatterns = [
        re.compile("선물과 메세지를 보냈습니다."),
        re.compile("선물을 보냈습니다.")
    ]

    emoticonPattern = re.compile("이모티콘\s*$")

    @staticmethod
    def IsGift(message: Message):
        for pattern in MessageUtil.giftPatterns:
            if pattern.match(message.getMessage()):
                return True
        return False
    
    @staticmethod
    def IsEmoticon(message: Message):
        return len(message.messageLines) == 1 and MessageUtil.emoticonPattern.match(message.messageLines[0]) is not None
