import os
import sys
sys.path.append('/Users/sudarshannagesh/miniconda3/lib/python3.12/site-packages')
import smtplib
from bs4 import BeautifulSoup
import lxml
import time
import tkinter.messagebox as msg
import datetime
import subprocess
current_folder = os.path.dirname(__file__)
sys.path.append(current_folder)

MY_EMAIL = 'ramgn2022@gmail.com'
PASSWORD = 'owhi dnil gukr nfol'
today = datetime.datetime.now()
response_file = r"response.html"
response_txt_file = r"response.txt"
if os.path.exists(response_txt_file):
    with open(response_txt_file, 'r') as f:
        f_str = f.read()
    if today.strftime('%Y%m%d') in f_str:
        sys.exit('Already checked for today.')


url = 'https://www.amazon.com/dp/1118008189/'
command = 'wget {0} -Outfile {1}'.format(url, response_file)

idx = 0
price_symbol_found = False
while idx < 5:
    try:
        if os.path.exists(response_file):
            os.remove(response_file)
        completed = subprocess.run(['powershell', '-Command', command],
                                   capture_output=True)
        if completed.returncode != 0:
            raise Exception
        with open(response_file, 'r', encoding='UTF-8') as f:
            f_str = f.read()
        soup = BeautifulSoup(f_str, 'lxml')
        all_spans = soup.find_all(name='span')
        classes = [span.get('class') for span in all_spans]
        # print(classes)
        for l_class in classes:
            if l_class and 'a-price-symbol' in l_class:
                price_symbol_found = True
                break
        if price_symbol_found:
            price_symbol = soup.find(name='span',
                                     class_='a-price-symbol').getText()
            price_whole = soup.find(name='span',
                                    class_='a-price-whole').getText()
            price_fraction = soup.find(name='span',
                                       class_='a-price-fraction').getText()
            price = 'price: {0}{1}{2}'.format(price_symbol,
                                              price_whole,
                                              price_fraction)
            price_whole = float(price_whole)
            with open(response_txt_file, 'a') as f:
                f.write('{0} {1}\n'.format(today.strftime('%Y%m%d'),
                                           price[7:]))
            print(price)
        else:
            raise Exception('Didnt find price_symbol')
    except Exception as e:
        print('Exception: ', e)
        idx += 1
        time.sleep(15)
    else:
        if price_whole < 10:
            message = 'Subject:Check this\n\nprice: {0}' \
                      '\nurl: {1}'.format(price,
                                          url)
            idx = 0
            while idx < 5:
                try:
                    with smtplib.SMTP("smtp.gmail.com") as connection:
                        connection.starttls()
                        connection.login(user=MY_EMAIL,
                                         password=PASSWORD)
                        connection.sendmail(from_addr=MY_EMAIL,
                                            to_addrs=
                                            'sudarshannagesh90@gmail.com',
                                            msg=message)
                except Exception as e:
                    print('Exception: ', e)
                    idx += 1
                else:
                    msg.showinfo('Price', 'Did sendmail for price')
                    sys.exit('Did sendmail')
            msg.showinfo('Price', 'Problem in sendmail for price')
        break

if not price_symbol_found:
    msg.showinfo('Price', 'Didnt find price symbol')
    sys.exit()
