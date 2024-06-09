from calendar import monthrange
import datetime as dt
from MessageHistory import MessageHistory

class InsightsByPeroid:
    def __init__(self, history: MessageHistory, periodStart: dt.date, peroidEnd: dt.date):
        self.periodStart = periodStart
        self.periodEnd = peroidEnd

        self.messages = [msg for msg in history.messages if periodStart <= msg.datetime.date() <= peroidEnd]

    def print(self):
        print()
        print(f'{self.periodStart} ~ {self.periodEnd}')
        print(f'message count: {len(self.messages)}')

    def createMonthly(history: MessageHistory):
        uniqueMonths = set()
        for msg in history.messages:
            yearMonth = f'{msg.datetime.year}-{msg.datetime.month}'
            uniqueMonths.add(yearMonth)
        
        for yearMonth in uniqueMonths:
            year, month = yearMonth.split('-')
            monthDays = monthrange(int(year), int(month))[1]
            start = dt.date(int(year), int(month), 1)
            end = dt.date(int(year), int(month), monthDays)
            yield InsightsByPeroid(history, start, end)

    
    def createYearly(history: MessageHistory):
        uniqueYears = set()
        for msg in history.messages:
            uniqueYears.add(msg.datetime.year)

        for year in uniqueYears:
            start = dt.date(year, 1, 1)
            end = dt.date(year, 12, 31)
            yield InsightsByPeroid(history, start, end)