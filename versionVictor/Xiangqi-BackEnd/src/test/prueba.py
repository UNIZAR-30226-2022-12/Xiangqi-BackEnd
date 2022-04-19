
import datetime


today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
dia = datetime.datetime.strptime('2022-03-17', '%Y-%m-%d').date()
print((yesterday- today).days)
