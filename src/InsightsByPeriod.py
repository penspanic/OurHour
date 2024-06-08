import datetime as dt
from MessageHistory import MessageHistory

class InsightsByPeroid:
    def __init__(self, history: MessageHistory, periodStart: dt.date, peroidEnd: dt.date):
        self.periodStart = periodStart
        self.periodEnd = peroidEnd

        self.messages = [msg for msg in history.messages if periodStart <= msg.datetime.date() <= peroidEnd]
    def createMonthly(history: MessageHistory):
        return [InsightsByPeroid(history, month, month + dt.timedelta(days=30)) for month in history.messagesByMonth.keys()]