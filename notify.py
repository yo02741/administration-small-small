from tabnanny import check
import requests
import datetime

date_format = '%Y-%m-%d'
today = datetime.date.today()
today_weekday_num = today.weekday()

message_list = []

class MessageItem():
  def __init__(self):
    self.Label = None
    self.Content = None

def notify_meeting_day():
  meeting_list = [
    '2023-01-12',
    '2023-02-09',
    '2023-03-09',
    '2023-04-13',
    '2023-05-11',
    '2023-06-15',
    '2023-07-13',
    '2023-08-10',
    '2023-09-14',
    '2023-10-12',
    '2023-11-09',
    '2023-12-14',
  ]
  for meeting_date_str in meeting_list:
    meeting_date = datetime.datetime.strptime(meeting_date_str, date_format).date()
    
    diff = (meeting_date - today).days
    
    if diff == 2:
      item = MessageItem()
      item.Label = '➭ 行政小小會議'
      item.Content = f'本週將於 {meeting_date} 舉行行政小小會議，若有同仁該時段有要事請提出並告知佩株學姐，謝謝。'
      message_list.append(item)


def notify_write_weekly_report():
  if today_weekday_num == 0:
    item = MessageItem()
    item.Label = '➭ 工作週報'
    item.Content = '請同仁於 14:00 前完成本週的工作週報，謝謝。'
    message_list.append(item)


def format_message_list():
  result_str = '\n\n '

  for (index, message_item) in enumerate(message_list):
    result_str += message_item.Label
    result_str += '\n'
    result_str += message_item.Content
    if len(message_list) - 1 > index:
      result_str += '\n\n'

  return result_str


def lineNotifyMessage(token, msg):
  headers = {
    'Authorization': 'Bearer ' + token, 
    'Content-Type' : 'application/x-www-form-urlencoded'
  }

  payload = {'message': msg }
  r = requests.post('https://notify-api.line.me/api/notify', headers = headers, params = payload)
  return r.status_code


if __name__ == '__main__':
  notify_meeting_day()
  notify_write_weekly_report()
  
  if len(message_list) == 0:
    pass
  else:
    token = ''
    lineNotifyMessage(token, format_message_list())