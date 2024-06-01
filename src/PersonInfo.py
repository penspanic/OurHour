import Messages
from typing import List
import datetime

class PersonInfo:
    def __init__(self, name: str, messages: List[Messages.Message]):
        self.name = name
        self.messages = messages

        replyTerms = [] # type: List[datetime.timedelta]
        for message in messages:
            if message.replyTerm is None:
                continue

            replyTerms.append(message.replyTerm)

        # replyTerms를 seconds로 변환
        # replyTerms = [term.total_seconds() for term in replyTerms]

        termSum = datetime.timedelta()
        for term in replyTerms:
            termSum += term

        #termSum = sum(replyTerms)
        termCount = len(replyTerms)
        print(f'replyTermNormalized = {termSum} / {termCount if termCount > 0 else None}')
        self.replyTermNormalized = termSum / termCount if termCount > 0 else None


class Comparison:
    def __init__(self, person1: PersonInfo, person2: PersonInfo):
        self.person1 = person1
        self.person2 = person2

        self.replyTermDiff = person1.replyTermNormalized - person2.replyTermNormalized if person1.replyTermNormalized is not None and person2.replyTermNormalized is not None else None

        # 비교 항목
        # 답장 텀(정규화)
        #  - 답장 텀 총합 / 메세지 개수