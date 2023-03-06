import requests
from datetime import date, datetime

TODAY = date.today()

MESSAGE_LIST = []


class MessageItem():
    def __init__(self, label=None, content=None):
        self.label = label
        self.content = content


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
        meeting_date = datetime.strptime(
            meeting_date_str, '%Y-%m-%d').date()

        diff = (meeting_date - TODAY).days

        if diff == 2:
            item = MessageItem()
            item.label = '➭ 行政小小會議'
            item.content = f'本週將於 {meeting_date} 舉行行政小小會議，若有同仁該時段有要事請提出並告知佩株學姐，謝謝。'
            MESSAGE_LIST.append(item)


def notify_write_weekly_report():
    if TODAY.weekday() == 0:
        item = MessageItem()
        item.label = '➭ 工作週報'
        item.content = '請同仁於 14:00 前完成本週的工作週報，謝謝。'
        MESSAGE_LIST.append(item)


def format_message_list():
    result_str = '\n\n '

    for (index, message_item) in enumerate(MESSAGE_LIST):
        result_str += f'{message_item.label} \n {message_item.content}'
        if len(MESSAGE_LIST) - 1 > index:
            result_str += '\n\n'

    return result_str


def line_notify_message(token, msg):
    headers = {
        'Authorization': 'Bearer ' + token,
        'content-Type': 'application/x-www-form-urlencoded'
    }

    payload = {'message': msg}
    r = requests.post('https://notify-api.line.me/api/notify', headers=headers, params=payload)
    return r.status_code


if __name__ == '__main__':
    notify_meeting_day()
    notify_write_weekly_report()

    if MESSAGE_LIST:
        token = ''
        line_notify_message(token, format_message_list())
