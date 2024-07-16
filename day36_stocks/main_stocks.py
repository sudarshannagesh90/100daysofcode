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

DAILY_STOCK_CSV_FOLDER = r"C:\Users\sudar\Desktop\DE_COURSE\100daysOfCode\day_36_stock-news-extrahard-start\daily_stock_csv_folder"
HISTORICAL_STOCKS_DB_FILE = r"C:\Users\sudar\Desktop\DE_COURSE\100daysOfCode\day_36_stock-news-extrahard-start\stocks.db"
HOLDING_STOCKS_DB_FILE = r"C:\Users\sudar\Desktop\git\cs50_sql\icicidirect\icicidirect.db"
NEWSDATA_API_KEY = 'pub_43877cda703284d325545f43b94eb04af2d73'
MY_EMAIL = 'ramgn2022@gmail.com'
PASSWORD = 'owhi dnil gukr nfol'

if not os.path.exists(DAILY_STOCK_CSV_FOLDER):
    os.mkdir(DAILY_STOCK_CSV_FOLDER)

db = sqlite3.connect(HOLDING_STOCKS_DB_FILE)
holding_stock_isin = db.cursor().execute(
    'SELECT "ISIN_CODE" FROM "STOCK";').fetchall()
db.close()
holding_stock_isin = [row[0] for row in holding_stock_isin]

def find_word_idx(words, given_word):
    for word_idx, word in enumerate(words):
        if word == given_word: return word_idx
    return None


def get_dict_from_data(f_lines):
    title_line = [word.strip().lower() for word in f_lines[0].split(',')]
    stock_symbol_idx = find_word_idx(title_line, 'TckrSymb'.strip().lower())
    isin_idx = find_word_idx(title_line, 'ISIN'.strip().lower())
    close_idx = find_word_idx(title_line, 'ClsPric'.strip().lower())
    previous_close_idx = find_word_idx(title_line, 'PrvsClsgPric'.strip().lower())
    if stock_symbol_idx is None or isin_idx is None or close_idx is None or\
        previous_close_idx is None:
        sys.exit('Dont have headings in file.')
    stocks_dict = {}
    for line in f_lines:
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
    month = yesterday.strftime('%b')
    # url = 'https://nsearchives.nseindia.com/content/historical/EQUITIES/{0}/{1}/cm{2}bhav.csv.zip'
    # url = url.format(year, month, file_name)
    url = 'https://www.nseindia.com/api/reports?archives=%5B%7B%22name%22%3A%22CM-UDiFF%20Common%20Bhavcopy%20Final%20(zip)%22%2C%22type%22%3A%22daily-reports%22%2C%22category%22%3A%22capital-market%22%2C%22section%22%3A%22equities%22%7D%5D&date={0}&type=equities&mode=single'.format(yesterday.strftime('%d-%b-%Y'))
    headers = requests.utils.default_headers()
    headers.update({'User-Agent': 'My User Agent 1.0'})
    idx = 0
    while idx < 10:
        try:
            response = requests.get(url, stream=True, headers=headers)
            response.raise_for_status()
        except Exception as e:
            print('Exception: ', e)
            time.sleep(60)
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
                csv_file = os.listdir(target_folder)[0]
                with open(os.path.join(target_folder, csv_file), 'r') as f:
                    return f.read().split('\n')
            except Exception as e:
                print('Exception: ', e)
                return None
    return None


today = datetime.datetime.now()
yesterday = today - datetime.timedelta(days=1)
checked_file = os.path.join(DAILY_STOCK_CSV_FOLDER, 'checked_for_today.txt')
if os.path.exists(checked_file):
    with open(checked_file, 'r') as f:
        f_lines = [elem.strip() for elem in f.read().split('\n')]
    if today.strftime('%Y%m%d') in f_lines:
        sys.exit('Have checked for today.')

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

db = sqlite3.connect(HISTORICAL_STOCKS_DB_FILE)
cursor = db.cursor()
results = cursor.execute('SELECT "STOCK_CODE", "STOCK_NAME", '
                         '"ISIN_CODE" FROM "STOCK";').fetchall()
STOCKS = [code[0] for code in results]
COMPANY_NAMES = [code[1] for code in results]
STOCKS_ISIN = [code[2] for code in results]

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
    cursor.execute(
        "INSERT INTO \"STOCK_PRICE\" VALUES('{0}','{1}','{2}');".format(STOCK, 
        yesterday_close_price, yesterday.strftime('%Y-%m-%d')))

    if ISIN_CODE not in holding_stock_isin:
        continue

    if abs(percent_change_in_price) < 5:
        print('{0}: {1:.2f}'.format(STOCK,
                                    abs(percent_change_in_price)))
        continue

    api_endpoint = 'https://newsdata.io/api/1/news?apikey={1}&qInMeta="{0}"&country=in'.format(COMPANY_NAME.replace('&', '%26'), NEWSDATA_API_KEY)

    idx = 0
    while idx < 5:
        try:
            json_data = requests.get(api_endpoint, timeout=5).json()
        except Exception as e:
            print('Exception: ', e)
            time.sleep(60)
            idx += 1
        else:
            for article in json_data['results'][:3]:
                title = article['title']
                description = article['description']
                url = article['link']
                top_three_news += 'Title: {0}\nDescription: {1}\nLink: {2}\n'.format(title, description, url)
            top_three_news = re.sub(r'[^\x00-\x7f]', r'', top_three_news)  # this is for the problem in top_three_news
            top_three_news += '\n\n'
            break

    stocks_with_change.append(STOCK)
    percent_changes_in_stocks.append(percent_change_in_price)

db.commit()
db.close()

with open(checked_file, 'a') as f:
    f.write(today.strftime('%Y%m%d\n'))

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
                                to_addrs='sudarshannagesh90@gmail.com',
                                msg=message)
    except Exception as e:
        print('Exception: ', e)
        time.sleep(60)
        idx += 1
    else:
        msg.showinfo(title='Stocks', message='Did sendmail')
        sys.exit()

if idx == 5:
    msg.showinfo(title='Stocks',
                 message='Seems exception in sendmail')
