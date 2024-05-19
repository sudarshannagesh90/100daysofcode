from utlty import get_symbol_name_for_isin
yahoo_isin = r'C:\Users\sudar\Desktop\DE_COURSE\100daysOfCode\day_36_stock-news-extrahard-start\csv_folder\yahoo_isin.csv'
CSV_FILE = r"C:\Users\sudar\Desktop\DE_COURSE\100daysOfCode\day_36_stock-news-extrahard-start\csv_folder\02MAY2024\cm02MAY2024bhav.csv"

isin_codes = []
with open(CSV_FILE, 'r') as f:
    f_lines = f.read().strip().split('\n')
    for f_line in f_lines[1:]:
        isin_codes.append(f_line.rstrip(',').split(',')[-1])

rows = [['Symbol', 'Longname', 'Shortname','ISIN']]
for isin_code in isin_codes:
    symbol, longname, shortname = get_symbol_name_for_isin(isin_code)
    if symbol and longname and shortname:
        print(symbol, longname, shortname, isin_code)
        rows.append([symbol, longname, shortname, isin_code])

rows_str = [','.join(row) for row in rows]
rows_str = '\n'.join(rows_str)

with open(yahoo_isin, 'w') as f:
    f.write(rows_str)
