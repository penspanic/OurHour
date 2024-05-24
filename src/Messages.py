import datetime

class Message:
    def __init__(self, sender: str, datetime: datetime.datetime, messageLines: str):
        self.sender = sender
        self.datetime = datetime
        self.messageLines = messageLines
    
    def getMessage(self):
        return '\n'.join(self.messageLines)

    def __str__(self):
        return f'{self.sender} {self.datetime} {self.getMessage()}'

    def __repr__(self):
        return f'{self.sender} {self.datetime} {self.getMessage()}'
    
class MessageHistory:
    def __init__(self):
        self.messages = []
        self.messagesByDate = {}

    def addMessage(self, message: Message):
        self.messages.append(message)
        dt = message.datetime.date()
        if dt not in self.messagesByDate:
            self.messagesByDate[dt] = []
        self.messagesByDate[dt].append(message)

    def __str__(self):
        return '\n'.join([str(message) for message in self.messages])

    def __repr__(self):
        return '\n'.join([str(message) for message in self.messages])