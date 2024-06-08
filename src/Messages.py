import datetime
import re
import typing

class MessageAttributes:
    gift = 'gift'
    emoticon = 'emoticon'
    suntalk = 'suntalk' # 선톡

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

class MessageUtil:
    emoticonPattern = re.compile("이모티콘\s*$")

    @staticmethod
    def IsGift(message: Message):
        messageStr = message.getMessage()
        if "선물과 메시지를 보냈습니다." in messageStr:
            return True
        if "선물을 보냈습니다." in messageStr:
            return True
        return False
    
    @staticmethod
    def IsEmoticon(message: Message):
        return len(message.messageLines) == 1 and MessageUtil.emoticonPattern.match(message.messageLines[0]) is not None
    
    @staticmethod
    def IsSunTalk(message: Message, messages: typing.List[Message], threshold: datetime.timedelta):
        if len(messages) == 0:
            return True
        
        # 메세지를 뒤에서부터 확인하면서 상대방이 보낸 마지막 메세지를 찾는다
        lastMessage = None
        for m in reversed(messages):
            if m.sender != message.sender:
                lastMessage = m
                break

        if lastMessage is None:
            return True
        
        return message.datetime - lastMessage.datetime > threshold