from typing import List
import re
import datetime as dt
import dateutil.parser
import Messages

class ChatParser:
    messageHeaderPattern = re.compile(r'\[(.*)\] \[([0-9]+:[0-9]+ (PM|AM))\] (.*)')
    # 2016. 7. 19. 오후 3:14, Sender : Message
    #                                     Year       Month      Date       오전/오후    Hour     Minute    Sender     Message
    messageHeaderPattern2 = re.compile(r'([0-9]+)\. ([0-9]+)\. ([0-9]+)\. (오전|오후) ([0-9]+):([0-9]+), (.*) : (.*)')
    
    #                                              Day(eng)  Month(eng)    Date(num)  Year(num)
    newDatePattern = re.compile(r'--------------- ([a-zA-Z]+), ([a-zA-Z]+) ([0-9]+), ([0-9]+) ---------------')
    #                               Year(num) Month(num) Date(num)
    newDataPattern2 = re.compile(r'([0-9]+)년 ([0-9]+)월 ([0-9]+)일')

    @staticmethod
    def parse(filePaths: List[str]):
        # [Name] [hh:mm AM/PM] [Message]
        return
    
    def parseOneFile(filePath : str):
        messagesByDate = {} # Key : date, Value : List of messages
        with open(filePath, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            # lines[0] : [Name] with KakaoTalk Chats
            # lines[1] : Data Saved : yyyy-mm-dd hh:mm:ss
            # lines[2] : <empty line>
            # lines[3] : 
            lines = lines[3:]
            
            messageHistory = Messages.MessageHistory()
            messageLines = None
            messageSender = ''
            messageDatetime = None
            for line in lines:
                newDateHeader = ChatParser.newDatePattern.match(line)
                if newDateHeader:
                    date = dateutil.parser.parse(newDateHeader.group(1) + " " + newDateHeader.group(2) + " " + newDateHeader.group(3) + " " + newDateHeader.group(4)).date()
                    thisDate = date
                    continue
                newDateHeader = ChatParser.newDataPattern2.match(line)
                if newDateHeader:
                    date = dateutil.parser.parse(newDateHeader.group(1) + "-" + newDateHeader.group(2) + "-" + newDateHeader.group(3)).date()
                    thisDate = date
                    continue

                messageHeader = ChatParser.messageHeaderPattern.match(line)
                if messageHeader:
                    if messageLines and len(messageLines) > 0:
                        msg = Messages.Message(messageSender, messageDatetime, messageLines)
                        messageHistory.addMessage(msg)
                    messageLines = []
                    messageSender = messageHeader.group(1)
                    messageDatetime = dateutil.parser.parse(messageHeader.group(2))
                    messageLines.append(messageHeader.group(4))
                    continue
                messageHeader = ChatParser.messageHeaderPattern2.match(line)
                if messageHeader:
                    if messageLines and len(messageLines) > 0:
                        msg = Messages.Message(messageSender, messageDatetime, messageLines)
                        messageHistory.addMessage(msg)
                    messageLines = []
                    messageSender = messageHeader.group(7)
                    ampm = messageHeader.group(4)
                    ampm = 'AM' if ampm == "오전" else 'PM'
                    dateStr = f'{messageHeader.group(1)}-{messageHeader.group(2)}-{messageHeader.group(3)} {messageHeader.group(5)}:{messageHeader.group(6)} {ampm}'

                    messageDatetime = dateutil.parser.parse(dateStr)
                    messageLines.append(messageHeader.group(8))
                    continue
                

                if messageLines:
                    messageLines.append(line)
            
            if len(messageLines) > 0:
                msg = Messages.Message(messageSender, messageDatetime, messageLines)
                messageHistory.addMessage(msg)

        return messageHistory

if __name__ == "__main__":
    history = ChatParser.parseOneFile("path-to-chat-file.txt")
    for date, messages in history.messagesByDate.items():
        print(date)
        for message in messages:
            print('\t', str(message))