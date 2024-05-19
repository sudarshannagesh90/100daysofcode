import datetime
import sqlite3
from smtplib import SMTP_SSL
import sys, os
from prettytable import PrettyTable, ALL
from email.message import EmailMessage

DB_FILE = r"C:\Users\sudar\Desktop\DE_COURSE\100daysOfCode\day_36_stock-news-extrahard-start\stocks.db"
ICICIDIRECT_DB_FILE = r"C:\Users\sudar\Desktop\git\cs50_sql\icicidirect\icicidirect.db"
MY_EMAIL = 'ramgn2022@gmail.com'
PASSWORD = 'owhi dnil gukr nfol'

def so(A, so_idx):
    len_A = len(A)
    if len_A == 1:
        return A
    return mrg(so(A[:len_A // 2], so_idx),
               so(A[len_A // 2:], so_idx),
               so_idx)


def mrg(C, D, so_idx):
    idx_c, idx_d, len_C, len_D, E = 0, 0, len(C), len(D), []
    while idx_c != len_C and idx_d != len_D:
        if C[idx_c][so_idx] > D[idx_d][so_idx]:
            E.append(C[idx_c])
            idx_c += 1
        else:
            E.append(D[idx_d])
            idx_d += 1
    if idx_c != len_C:
        E.extend(C[idx_c:])
    else:
        E.extend(D[idx_d:])
    return E

today = datetime.datetime.now()
if today.strftime('%a') != 'Sat':
    sys.exit('Exiting. Today is not Saturday.')
checked_for_today = r"C:\Users\sudar\Desktop\DE_COURSE\100daysOfCode\day_98_custom_automate\checked_for_today.txt"
if os.path.exists(checked_for_today):
    with open(checked_for_today, 'r') as f:
        f_lines = [f_line for f_line in f.read().strip().split('\n')]
        for f_line in f_lines:
            if f_line.strip() == today.strftime('%Y-%m-%d'):
                sys.exit('Exiting. Have checked for today.')

db = sqlite3.connect(ICICIDIRECT_DB_FILE)
cursor = db.cursor()
results = cursor.execute('SELECT "ISIN_CODE" FROM "STOCK";').fetchall()
icici_isin_codes = [code[0] for code in results]
db.close()

db = sqlite3.connect(DB_FILE)
cursor = db.cursor()
results = cursor.execute('SELECT "STOCK_CODE", "STOCK_NAME", "ISIN_CODE" '
                         'FROM "STOCK";').fetchall()
query = 'SELECT "CLOSE_PRICE" FROM "STOCK_PRICE" WHERE ' \
        '"TIMESTAMP">=\'{0}\' AND "STOCK_CODE"=\'{1}\'' \
        'ORDER BY "TIMESTAMP";'
percent_table = PrettyTable(field_names=['Stock',
                                         '1W', '1M', '3M', '6M',
                                         '1Y', '3Y',
                                         'Full', 'Close_Price'])
percent_table_other_stocks = PrettyTable(field_names=['Stock','Stock_name',
                                         '1W', '1M', '3M', '6M',
                                         '1Y', '3Y',
                                         'Full', 'Close_Price'])
percent_table_rows = []
percent_table_other_stocks_rows = []
for stock_code, stock_name, isin_code in results:
    didnt_find_prices = False
    percent_changes = [stock_code, stock_name]
    close_price = None
    for days in [7, 30, 90, 180, 365, 365 * 3, 3650]:
        start_date = (today - datetime.timedelta(days=days)).strftime(
            '%Y-%m-%d')
        close_prices = cursor.execute(query.format(start_date,
                                                   stock_code)).fetchall()
        if len(close_prices) == 0:
            didnt_find_prices = True
            break
        close_prices = [price[0] for price in close_prices]
        close_price = close_prices[-1]
        percent_change = 100 * (close_prices[-1] - close_prices[0]) / \
                         close_prices[0]
        percent_changes.append(percent_change)
    if didnt_find_prices:
        continue
    if isin_code not in icici_isin_codes:
        percent_table_other_stocks_rows.append(percent_changes + [close_price])
    else:
        percent_table_rows.append(percent_changes + [close_price])

percent_table_rows = so(percent_table_rows, -3)
for row in percent_table_rows:
    row = [row[0]] + ['{0:.2f}%'.format(elem) for elem in row[2:-1]] + [row[-1]]
    row[-1] = '{0:.2f}'.format(row[-1])
    percent_table.add_row(row)

percent_table_other_stocks_rows = so(percent_table_other_stocks_rows,
                                     -3)
for row in percent_table_other_stocks_rows:
    row[2:-1] = ['{0:.2f}%'.format(elem) for elem in row[2:-1]]
    row[-1] = '{0:.2f}'.format(row[-1])
    percent_table_other_stocks.add_row(row)

percent_table_str = percent_table.get_formatted_string('html', header=True,
                                                       border=True,
                                               preserve_internal_border=True,
                                               hrules=ALL,
                                               format=True)
percent_table_other_stocks_str = \
    percent_table_other_stocks.get_formatted_string('html', header=True,
                                                    border=True,
                                            preserve_internal_border=True,
                                            hrules=ALL,
                                            format=True)
msg = EmailMessage()
msg['Subject'] = 'Weekly-change {0}'.format(today.strftime('%Y-%m-%d'))
msg['From'] = MY_EMAIL
msg['To'] = 'sudarshannagesh90@gmail.com'
msg.set_content(percent_table_str + '<br><br>' + \
                percent_table_other_stocks_str, subtype='html')
trial_idx = 0
while trial_idx < 5:
    try:
        with SMTP_SSL('SMTP.gmail.com') as connection:
            connection.login(MY_EMAIL, PASSWORD)
            connection.send_message(msg)
    except Exception as e:
        print('Exception: ', e)
        trial_idx += 1
    else:
        break

with open(checked_for_today, 'a') as f:
    f.write(today.strftime('%Y-%m-%d') + '\n')
