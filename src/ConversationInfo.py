from MessageHistory import MessageHistory


class ConversationInfo:
    def create(history: MessageHistory, myName: str):
        yourName = history.messagesBySender.keys() - {myName}
        if len(yourName) == 0:
            return None
        yourName = yourName.pop()
        return ConversationInfo(history, myName, yourName)

    def __init__(self, history: MessageHistory, myName: str, yourName: str) -> None:
        self.myMessages = [message for message in history.messages if message.sender == myName]
        self.yourMessages = [message for message in history.messages if message.sender == yourName]

        self.messageRatio = len(self.myMessages) / len(self.yourMessages) if len(self.yourMessages) > 0 else None
    
    def asDict(self):
        return {
            '내 메세지 수': len(self.myMessages),
            '상대방 메세지 수': len(self.yourMessages),
            '메세지 비율( > 1 : 내가 더 많은 메세지)': self.messageRatio
        }
