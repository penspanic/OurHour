from MessageHistory import MessageHistory
from PersonInfo import PersonInfo
from factory import createPersonInfo


class ConversationInfo:
    def __init__(self, me: PersonInfo, you: PersonInfo) -> None:
        self.me = me
        self.you = you
        self.messageRatioDesc = '메세지 비율( > 100 : 내가 더 많은 메세지)'
        self.messageRatio = len(me.messages) / len(you.messages) if len(you.messages) > 0 else None

        self.messageLengthRatioDesc = '평균 메세지 길이 비율( > 100 : 내가 더 긴 메세지)'
        self.messageLengthRatio = me.averageMessageLength / you.averageMessageLength if you.averageMessageLength is not None else None

        self.replyTermRatioDesc = '답장 텀 비율( > 100 : 내가 더 빠른 답장)'
        self.replyTermRatio = you.replyTermNormalized / me.replyTermNormalized if me.replyTermNormalized is not None else None
    
    def asDict(self):
        return {
            self.messageRatioDesc: f'{(self.messageRatio * 100):2f} %',
            self.messageLengthRatioDesc: f'{(self.messageLengthRatio * 100):2f} %' if self.messageLengthRatio is not None else '에러',
            self.replyTermRatioDesc:     f'{(self.replyTermRatio * 100):2f} %' if self.replyTermRatio is not None else '에러'
        }
    def asDictWithScore(self):
        d = self.asDict()
        d[self.messageRatioDesc] = (d[self.messageRatioDesc], self.messageRatioScore())
        d[self.messageLengthRatioDesc] = (d[self.messageLengthRatioDesc], self.messageLengthRatioScore())
        d[self.replyTermRatioDesc] = (d[self.replyTermRatioDesc], self.replyTermRatioScore())
        return d

    
    def messageRatioScore(self):
        return int((self.messageRatio - 1) / 0.05)
    def messageLengthRatioScore(self):
        return int((self.messageLengthRatio - 1) / 0.05)
    def replyTermRatioScore(self):
        return int((self.replyTermRatio - 1) / 0.05)