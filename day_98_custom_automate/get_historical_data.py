import os, subprocess

CSV_FILE = r"C:\Users\sudar\Desktop\DE_COURSE\100daysOfCode\day_36_stock-news-extrahard-start\csv_folder\yahoo_isin.csv"
CSV_FOLDER = r"C:\Users\sudar\Desktop\DE_COURSE\100daysOfCode\day_36_stock-news-extrahard-start\csv_folder\historical_yahoo_data"
# note the url period has to be changes appropriately? Done on May 17, 2024
url = 'https://query1.finance.yahoo.com/v7/finance/download/{0}?period1=1558076145"&"period2=1715923164"&"interval=1d"&"events=history"&"includeAdjustedClose=true'

command_str = 'wget {0} -Outfile {1}'
problem_idx = 0
with open(CSV_FILE, 'r') as f:
    f_lines = f.read().strip().split('\n')
    for f_line in f_lines[1:]:
        symbol = f_line.split(',')[0]
        response_file = os.path.join(CSV_FOLDER, '{0}.csv'.format(symbol))
        command = command_str.format(url.format(symbol.replace('&', '%26')),
                                     response_file)
        completed = subprocess.run(['powershell', '-Command', command],
                                   capture_output=True)
        if completed.returncode != 0:
            print('Problem in: ', symbol)
            problem_idx += 1
        else:
            print('Done for: ', symbol)

print('problem_idx: ', problem_idx)
