import requests
import datetime
import time
import sys
import smtplib
import os
import zipfile
import re
import sqlite3
from tkinter import messagebox as msg
current_folder = os.path.split(__file__)[0]

DAILY_STOCK_CSV_FOLDER = os.path.join(current_folder, 
    'daily_stock_csv_folder')
HOLDING_STOCK_CSV_FILE = os.path.join(current_folder,
    'holding_stock.csv')
NEWSDATA_API_KEY = 'TO_BE_FILLED'
MY_EMAIL = 'TO_BE_FILLED'
PASSWORD = 'TO_BE_FILLED'
TO_EMAIL = 'TO_BE_FILLED'
URL_ENDPOINT = 'https://newsdata.io/api/1/news?apikey={1}&qInMeta="{0}"&country=in'
DOWNLOAD_URL = 'https://nsearchives.nseindia.com/content/historical/EQUITIES/{0}/{1}/cm{2}bhav.csv.zip'

if not os.path.exists(DAILY_STOCK_CSV_FOLDER): os.mkdir(DAILY_STOCK_CSV_FOLDER)

def find_word_idx(words, given_word):
    for word_idx, word in enumerate(words):
        if word == given_word: return word_idx
    return None


def get_dict_from_data(f_lines):
    title_line = [word.strip().lower() for word in f_lines[0].split(',')]
    stock_symbol_idx = find_word_idx(title_line, 'symbol')
    isin_idx = find_word_idx(title_line, 'isin')
    close_idx = find_word_idx(title_line, 'close')
    previous_close_idx = find_word_idx(title_line, 'prevclose')
    if stock_symbol_idx is None or isin_idx is None or close_idx is None or\
        previous_close_idx is None:
        sys.exit('Dont have headings in file.')
    stocks_dict = {}
    for line in f_lines[1:]:
        if line:
            line = line.split(',')
            stocks_dict[line[isin_idx]] = {'SYMBOL': line[stock_symbol_idx],
                                           'CLOSE': line[close_idx],
                                           'PREVCLOSE':
                                               line[previous_close_idx]}
    return stocks_dict

def get_data():
    file_name = yesterday.strftime('%d%b%Y').upper()
    year = yesterday.strftime('%Y')
    month = yesterday.strftime('%b').upper()
    url = DOWNLOAD_URL.format(year, month, file_name)
    headers = requests.utils.default_headers()
    headers.update({'User-Agent': 'My User Agent 1.0'})
    idx = 0
    while idx < 5:
        try:
            response = requests.get(url, stream=True, headers=headers)
            response.raise_for_status()
        except Exception as e:
            print('Exception: ', e)
            idx += 1
        else:
            full_file_name = os.path.join(DAILY_STOCK_CSV_FOLDER,
                                          file_name + '_file.csv.zip')
            target_folder = os.path.join(DAILY_STOCK_CSV_FOLDER, file_name)
            try:
                with open(full_file_name, 'wb') as f:
                    for chunk in response.iter_content(128):
                        f.write(chunk)
                with zipfile.ZipFile(full_file_name) as zip_file:
                    zip_file.extractall(target_folder)
                os.remove(full_file_name)
                csv_file = os.listdir(target_folder)[0]
                with open(os.path.join(target_folder, csv_file), 'r') as f:
                    return f.read().split('\n')
            except Exception as e:
                print('Exception: ', e)
                return None
    return None


today = datetime.datetime.now()
yesterday = today - datetime.timedelta(days=1)
yesterday_f_lines = get_data()
if not yesterday_f_lines:
    sys.exit('Dont have data for yesterday.')
try:
    yesterday_stock_dict = get_dict_from_data(yesterday_f_lines)
except Exception as e:
    print('Exception: ', e)
    sys.exit('Unable to get dict from data.')

stocks_with_change = []
percent_changes_in_stocks = []
top_three_news = ''
news_str = 'Title: {0}\nDescription: {1}\nLink: {2}\n'

with open(HOLDING_STOCK_CSV_FILE, 'r') as f:
    f_lines = f.read().strip().split('\n')
    f_lines = [f_line.split(',') for f_line in f_lines]

STOCKS = [code[0] for code in f_lines]
COMPANY_NAMES = [code[3] for code in f_lines]
STOCKS_ISIN = [code[2] for code in f_lines]

for STOCK, COMPANY_NAME, ISIN_CODE in zip(STOCKS, COMPANY_NAMES, STOCKS_ISIN):
    try:
        yesterday_close_price = float(
            yesterday_stock_dict[ISIN_CODE]['CLOSE'])
        previous_day_close_price = float(
            yesterday_stock_dict[ISIN_CODE]['PREVCLOSE'])
    except Exception as e:
        print('Exception: ', e)
        print('Dont have prices for {0}'.format(STOCK))
        continue
    percent_change_in_price = 100 * (yesterday_close_price -
                                     previous_day_close_price) / \
                              previous_day_close_price
    if abs(percent_change_in_price) < 5:
        print('{0}: {1:.2f}'.format(STOCK,
                                    abs(percent_change_in_price)))
        continue

    api_endpoint = URL_ENDPOINT.format(COMPANY_NAME.replace('&', '%26'), 
        NEWSDATA_API_KEY)

    idx = 0
    while idx < 5:
        try:
            json_data = requests.get(api_endpoint, timeout=5).json()
            len(json_data['results'])
        except Exception as e:
            print('Exception: ', e)
            time.sleep(60)
            idx += 1
        else:
            for article in json_data['results'][:3]:
                title = article['title']
                description = article['description']
                url = article['link']
                top_three_news += news_str.format(title, description, url)
            top_three_news += '\n\n'
            break

    stocks_with_change.append(STOCK)
    percent_changes_in_stocks.append(percent_change_in_price)

if not len(stocks_with_change):
    msg.showinfo(title='Stocks',
                 message='Dont have stocks with change')
    sys.exit()

subject = ['{0}:{1:.2f}%'.format(stock, percent_change)
           for stock, percent_change in zip(stocks_with_change, 
            percent_changes_in_stocks)]
message = 'Subject: {0}\n\n{1}'.format(';'.join(subject), top_three_news)
idx = 0
while idx < 5:
    try:
        with smtplib.SMTP('smtp.gmail.com') as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL,
                                to_addrs=TO_EMAIL,
                                msg=message)
    except Exception as e:
        print('Exception: ', e)
        time.sleep(60)
        idx += 1
    else:
        msg.showinfo(title='Stocks', message='Did sendmail')
        sys.exit()
