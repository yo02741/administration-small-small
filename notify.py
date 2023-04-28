import requests
from datetime import date, datetime

TODAY = date.today()

NOW_HOUR = datetime.now().hour
NOW_MINUTE = datetime.now().minute

IS_EIGTH_THIRTY_AM = NOW_HOUR == 8 and NOW_MINUTE == 30
IS_TEN_AM = NOW_HOUR == 10 and NOW_MINUTE == 0
IS_ONE_THIRTY_PM = NOW_HOUR == 13 and NOW_MINUTE == 30
IS_FIVE_THIRTY_PM = NOW_HOUR == 17 and NOW_MINUTE == 30

MESSAGE_LIST = []


class MessageItem():
    def __init__(self, label=None, content=None):
        self.label = label
        self.content = content


def notify_meeting_day():
    """行政小小會議
    每個月的第二個禮拜四前兩天提醒"""
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
    """工作週報
    每週一早上跟下午提醒"""
    if TODAY.weekday() == 0:
        item = MessageItem()
        item.label = '➭ 工作週報'
        item.content = '請同仁於 14:00 前完成本週的工作週報，謝謝。'
        MESSAGE_LIST.append(item)


def notify_wirte_misson_management():
    """任務管理
    每個月18跟20號提醒"""
    if TODAY.day in [18, 20]:
        item = MessageItem()
        item.label = '➭ 任務管理'
        item.content = '請需要撰寫任務管理的同仁於 20 號前完成，不要跟錢錢過意不去。'
        MESSAGE_LIST.append(item)

def notify_schedule():
    """排班
    每個月的23跟25號提醒"""
    if TODAY.day in [23, 25]:
        item = MessageItem()
        item.label = '➭ 排班排班'
        item.content = '請同仁於 25 號前完成排班。'
        MESSAGE_LIST.append(item)


def notify_booking_lunch():
    """午餐預約"""
    if TODAY.weekday() in [0, 1, 2, 3, 4]:
        item = MessageItem()
        item.label = '➭ 訂午餐'
        item.content = '十點嚕，記得訂午餐，有團購的話不要理我。'
        MESSAGE_LIST.append(item)


def notify_weekend():
    """週末愉快"""
    if TODAY.weekday() == 4:
        item = MessageItem()
        item.label = '➭ 週末愉快'
        item.content = '今天是禮拜五，沒有人禮拜五加班的快回家，週末愉快。'
        MESSAGE_LIST.append(item)


def format_message_list() -> str:
    """組合提醒訊息"""
    result_str = '\n\n '

    for (index, message_item) in enumerate(MESSAGE_LIST):
        result_str += f'{message_item.label} \n {message_item.content}'
        if len(MESSAGE_LIST) - 1 > index:
            result_str += '\n\n'

    return result_str


def line_notify_message(token: str, msg: str):
    """發送 LINE 通知"""
    headers = {
        'Authorization': 'Bearer ' + token,
        'content-Type': 'application/x-www-form-urlencoded'
    }

    payload = {'message': msg}
    r = requests.post('https://notify-api.line.me/api/notify', headers=headers, params=payload)
    return r.status_code


if __name__ == '__main__':
    if IS_EIGTH_THIRTY_AM:
        notify_meeting_day()
        notify_write_weekly_report()
        notify_wirte_misson_management()
        notify_schedule()
    elif IS_TEN_AM:
        notify_booking_lunch()
    elif IS_ONE_THIRTY_PM:
        notify_write_weekly_report()
    elif IS_FIVE_THIRTY_PM:
        notify_weekend()

    if MESSAGE_LIST:
        token = ''
        line_notify_message(token, format_message_list())
