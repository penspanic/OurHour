from typing import List
import re
import datetime as dt
import dateutil.parser
from InsightsByPeriod import InsightsByPeriod
from MessageHistory import MessageHistory
from ConversationInfo import ConversationInfo
import Messages
import Utils
import os
from pathlib import Path

class ChatParser:
    messageHeaderPattern = re.compile(r'\[(.*)\] \[([0-9]+:[0-9]+ (PM|AM))\] (.*)')
    # 2016. 7. 19. 오후 3:14, Sender : Message
    #                                     Year       Month      Date       오전/오후    Hour     Minute    Sender     Message
    messageHeaderPattern2 = re.compile(r'([0-9]+)\. ([0-9]+)\. ([0-9]+)\. (오전|오후) ([0-9]+):([0-9]+), (.*?) : (.*)')
    #messageHeaderPattern2 = re.compile(r'([0-9]+)\. ([0-9]+)\. ([0-9]+)\. (오전|오후) ([0-9]+):([0-9]+), (.*) : (.*)')
    
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
            
            messageHistory = MessageHistory()
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
                    if messageLines is not None and len(messageLines) > 0:
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
    # get args.txt in same directory
    argsContent = None
    p = Path(__file__).with_name('args.txt')
    with p.open('r', encoding='utf-8') as f:
        argsContent = f.read()

    history = ChatParser.parseOneFile(argsContent)
    # for date, messages in history.messagesByDate.items():
    #     print(date)
    #     for message in messages:
    #         print('\t', str(message))

    personInfos = Utils.createPersonInfos(history)
    for personInfo in personInfos:
        personInfo.print()
    
    monthlyInsights = InsightsByPeriod.createMonthly(history)
    for monthlyInsight in monthlyInsights:
        monthlyInsight.print()
        
    yearlyInsights = InsightsByPeriod.createYearly(history)
    for yearlyInsight in yearlyInsights:
        yearlyInsight.print()

    conversationInfo = ConversationInfo.create(history, '박근희')
    if conversationInfo:
        print(conversationInfo.asDict())
    else:
        print('No conversation found')