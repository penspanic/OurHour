from typing import List
import re
import datetime as dt
import dateutil.parser
import Messages

class ChatParser:
    messageHeaderPattern = re.compile(r'\[(.*)\] \[([0-9]+:[0-9]+ (PM|AM))\] (.*)')
    #                                              Day(eng)  Month(eng)    Date(num)  Year(num)
    newDatePattern = re.compile(r'--------------- ([a-zA-Z]+), ([a-zA-Z]+) ([0-9]+), ([0-9]+) ---------------')

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
            messageLines = []
            messageSender = ''
            messageDatetime = None
            for line in lines:
                newDateHeader = ChatParser.newDatePattern.match(line)
                if newDateHeader:
                    date = dateutil.parser.parse(newDateHeader.group(1) + " " + newDateHeader.group(2) + " " + newDateHeader.group(3) + " " + newDateHeader.group(4)).date()
                    thisDate = date
                    continue

                messageHeader = ChatParser.messageHeaderPattern.match(line)
                if messageHeader:
                    if len(messageLines) > 0:
                        msg = Messages.Message(messageSender, messageDatetime, messageLines)
                        messageHistory.addMessage(msg)
                        messageLines = []
                    messageSender = messageHeader.group(1)
                    messageDatetime = dateutil.parser.parse(messageHeader.group(2))
                    messageLines.append(messageHeader.group(4))
                else: # multiline message
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
            print('\t', message)