from bs4 import BeautifulSoup
from datetime import datetime
import pprint
import re
import requests
import pytz

tz = pytz.timezone('Japan')
BASE_URL='https://ske48.co.jp'

def get_schedule_by_month_year(month: int, year: int) -> dict:
    return_dict = {}

    page = requests.get(BASE_URL + f'/schedule/list/{year}/{month}/')
    soup = BeautifulSoup(page.content, 'html.parser')

    for day in soup.find_all('li', class_='schedule_entry_box'):
        md = day.find('span', class_='md').get_text()
        dow = day.find('span', class_='week').get_text()
        return_dict[md] = {'dow' : dow,
                           'entries' : []
                          }
        for entry in day.find_all('div', class_='entry'):
            cat = entry.find('p', class_='cat').get_text()
            title = entry.find('p', class_='tit').get_text()
            url = entry.find('a')['href']
            return_dict[md]['entries'].append({'cat' : cat, 'title' : title,
                                               'url' : BASE_URL + url})
    return return_dict

def get_schedule_by_month(month: int) -> dict:
    return(get_schedule_by_month_year(month, datetime.now(tz).year))

def get_schedule() -> dict:
    return(get_schedule_by_month(datetime.now(tz).month))

def schedule_to_str(schedule: dict) -> str:
    return_str = ''
    for day in list(schedule.keys()):
        date_str = 'TODAY' if (int(day) == datetime.now(tz).day) else f"{day} {schedule[day]['dow']}"
        return_str += (date_str + '\n\n')
        for entry in schedule[day]['entries']:
            return_str += f"{entry['cat']}\n  {entry['title']} <{entry['url']}>\n"
    return return_str

def todays_schedule_str() -> str:
    schedule = get_schedule()
    today = str(datetime.now(tz).day)
    schedule = {today: schedule[today]}
    return schedule_to_str(schedule)

if __name__ == '__main__':
    print(todays_schedule_str())
